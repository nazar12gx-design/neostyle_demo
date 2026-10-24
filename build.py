#!/usr/bin/env python3
"""Генератор статического сайта NeoStyle KG.

Использование:
    python build.py            # собрать сайт в папку dist/
    python build.py --serve    # собрать и открыть http://localhost:8000
    python build.py --check    # собрать и проверить внутренние ссылки
    python build.py --stats    # показать размер файлов после сборки

Для Render: Static Site, Build Command = `python build.py`, Publish Directory = `dist`.
"""
import argparse
import functools
import http.server
import re
import shutil
import socketserver
import sys
import time
from datetime import date
from pathlib import Path

import templates as t
from assets import CSS, JS
from config import BRAND, PRODUCTS

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"


class Builder:
    """Собирает страницы и ассеты, хранит список созданных файлов."""

    def __init__(self, out=DIST):
        self.out = Path(out)
        self.files = []

    # ---------- базовые операции ----------
    def clean(self):
        if self.out.exists():
            shutil.rmtree(self.out)
        self.out.mkdir(parents=True)

    def write(self, rel, content):
        target = self.out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        self.files.append(target)

    @staticmethod
    def minify_css(css):
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        css = re.sub(r"\s+", " ", css)
        return re.sub(r"\s*([{};:,>])\s*", r"\1", css).strip()

    @staticmethod
    def minify_js(js):
        lines = [ln.strip() for ln in js.splitlines()]
        lines = [ln for ln in lines if ln and not ln.startswith("//")]
        return "\n".join(lines)

    # ---------- сборка ----------
    def build_assets(self):
        self.write("assets/style.css", self.minify_css(CSS))
        self.write("assets/app.js", self.minify_js(JS))
        self.write("assets/favicon.svg", t.favicon())

    def build_pages(self):
        self.write("index.html", t.page_home())
        self.write("catalog/index.html", t.page_catalog())
        self.write("about/index.html", t.page_about())
        self.write("contacts/index.html", t.page_contacts())
        self.write("404.html", t.page_404())
        for product in PRODUCTS:
            self.write(f"product/{product['id']}/index.html", t.page_product(product))

    def build_seo(self):
        base = BRAND["site_url"].rstrip("/")
        today = date.today().isoformat()
        urls = ["", "catalog/", "about/", "contacts/"] + [f"product/{p['id']}/" for p in PRODUCTS]
        items = "\n".join(
            f"  <url><loc>{base}/{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
        self.write("sitemap.xml",
                   '<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                   f"{items}\n</urlset>\n")
        self.write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")

    def build(self):
        started = time.perf_counter()
        self.clean()
        self.build_assets()
        self.build_pages()
        self.build_seo()
        elapsed = (time.perf_counter() - started) * 1000
        print(f"✔ Собрано файлов: {len(self.files)} за {elapsed:.0f} мс → {self.out}")
        return self.files


# ---------- проверки ----------
HREF_RE = re.compile(r'(?:href|src)="([^"#]+)(?:#[^"]*)?"')


def resolve(page, link, out):
    """Преобразует ссылку на странице в путь внутри dist/. None — внешняя ссылка."""
    if re.match(r"^(https?:|mailto:|tel:|data:|javascript:)", link):
        return None
    if link.startswith("/"):
        target = out / link.lstrip("/")
    else:
        target = (page.parent / link).resolve()
    if target.is_dir():
        target = target / "index.html"
    return target


def check_links(out):
    """Проверяет, что все внутренние ссылки ведут на существующие файлы."""
    out = Path(out).resolve()
    broken, checked = [], 0
    for page in out.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for link in HREF_RE.findall(text):
            target = resolve(page, link, out)
            if target is None:
                continue
            checked += 1
            if not target.exists():
                broken.append((page.relative_to(out), link))
    print(f"Проверено внутренних ссылок: {checked}")
    if broken:
        print("✖ Битые ссылки:")
        for page, link in broken:
            print(f"   {page}: {link}")
        return False
    print("✔ Битых ссылок нет")
    return True


def validate_content():
    """Базовая проверка данных в config.py: уникальные id, корректные цены."""
    errors, seen = [], set()
    for p in PRODUCTS:
        if p["id"] in seen:
            errors.append(f"Дублирующийся id: {p['id']}")
        seen.add(p["id"])
        if not re.fullmatch(r"[a-z0-9-]+", p["id"]):
            errors.append(f"id должен содержать только a-z, 0-9 и дефис: {p['id']}")
        if p["price"] <= 0:
            errors.append(f"Некорректная цена у {p['id']}")
        if p["old_price"] and p["old_price"] <= p["price"]:
            errors.append(f"Старая цена должна быть выше новой: {p['id']}")
        if not p["sizes"] or not p["colors"]:
            errors.append(f"Нет размеров или цветов: {p['id']}")
    for err in errors:
        print("✖", err)
    return not errors


def print_stats(out):
    out = Path(out)
    rows = sorted(((f.stat().st_size, f.relative_to(out)) for f in out.rglob("*") if f.is_file()),
                  reverse=True)
    total = sum(size for size, _ in rows)
    print(f"{'Файл':48}{'Размер':>10}")
    for size, name in rows[:12]:
        print(f"{str(name):48}{size / 1024:>8.1f} КБ")
    print(f"{'ИТОГО (' + str(len(rows)) + ' файлов)':48}{total / 1024:>8.1f} КБ")


def serve(out, port=8000):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Открой http://localhost:{port}  (Ctrl+C — остановить)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Сборка статического сайта NeoStyle KG")
    parser.add_argument("--serve", action="store_true", help="запустить локальный сервер")
    parser.add_argument("--check", action="store_true", help="проверить внутренние ссылки")
    parser.add_argument("--stats", action="store_true", help="показать размеры файлов")
    parser.add_argument("--port", type=int, default=8000, help="порт для --serve")
    args = parser.parse_args(argv)

    if not validate_content():
        return 1
    Builder().build()
    ok = True
    if args.check:
        ok = check_links(DIST)
    if args.stats:
        print_stats(DIST)
    if args.serve:
        serve(DIST, args.port)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
