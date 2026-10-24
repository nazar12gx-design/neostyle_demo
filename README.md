# NeoStyle KG — демо статического сайта

Генератор на Python (без внешних зависимостей) → папка `dist/`.

## Локально
    python build.py --check --stats
    python build.py --serve

## Render
1. Залей папку в GitHub.
2. New → Static Site → выбери репозиторий.
3. Build Command: `python build.py`  ·  Publish Directory: `dist`
   (или используй `render.yaml` через Blueprint).

Тексты, цены, контакты — в `config.py`.
