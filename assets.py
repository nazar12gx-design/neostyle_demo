"""CSS и JavaScript сайта (хранятся строками, build.py записывает их в dist/assets)."""

CSS = """
:root{--bg:#faf8fc;--fg:#1b1325;--muted:#6d647a;--card:#fff;--line:#e8e2f0;
--accent:#7c3aed;--accent2:#ec4899;--radius:18px;--shadow:0 10px 30px rgba(60,20,110,.10);
--max:1160px}
:root[data-theme="dark"]{--bg:#0f0b17;--fg:#f3effa;--muted:#a79cb8;--card:#181225;
--line:#2a2140;--shadow:0 10px 30px rgba(0,0,0,.45)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);
color:var(--fg);line-height:1.6;-webkit-font-smoothing:antialiased}
img,svg{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--max);margin:0 auto;padding:0 20px}
h1,h2,h3{line-height:1.15;letter-spacing:-.02em}
h1{font-size:clamp(2.2rem,6vw,4rem)}
h2{font-size:clamp(1.6rem,3.5vw,2.3rem);margin-bottom:12px}
.lead{color:var(--muted);font-size:1.1rem;max-width:620px}
.grad{background:linear-gradient(90deg,var(--accent),var(--accent2));
-webkit-background-clip:text;background-clip:text;color:transparent}
section{padding:64px 0}
.btn{display:inline-flex;align-items:center;gap:8px;padding:13px 24px;border-radius:999px;
border:0;font:inherit;font-weight:600;cursor:pointer;transition:.2s transform,.2s box-shadow}
.btn:hover{transform:translateY(-2px)}
.btn-primary{background:linear-gradient(90deg,var(--accent),var(--accent2));color:#fff;
box-shadow:0 8px 22px rgba(124,58,237,.35)}
.btn-ghost{background:transparent;border:1.5px solid var(--line);color:var(--fg)}
.btn-wa{background:#25d366;color:#08331a}
.header{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 88%,transparent);
backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.header .wrap{display:flex;align-items:center;justify-content:space-between;height:68px}
.logo{font-weight:800;font-size:1.3rem;letter-spacing:-.03em}
.nav{display:flex;gap:6px;align-items:center}
.nav a{padding:8px 14px;border-radius:999px;color:var(--muted);font-weight:500}
.nav a:hover,.nav a.active{color:var(--fg);background:var(--card)}
.tools{display:flex;gap:8px;align-items:center}
.icon-btn{position:relative;width:42px;height:42px;border-radius:50%;border:1px solid var(--line);
background:var(--card);cursor:pointer;font-size:1.1rem;color:var(--fg)}
.count{position:absolute;top:-4px;right:-4px;min-width:20px;height:20px;border-radius:10px;
background:var(--accent2);color:#fff;font-size:.72rem;display:grid;place-items:center;padding:0 5px}
.burger{display:none}
.hero{padding:80px 0 56px;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;inset:-20% -10% auto auto;width:520px;height:520px;
background:radial-gradient(circle,rgba(236,72,153,.28),transparent 65%);z-index:-1}
.hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.hero .btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.hero-art{border-radius:28px;overflow:hidden;box-shadow:var(--shadow);aspect-ratio:4/5}
.stats{display:flex;gap:32px;margin-top:36px;flex-wrap:wrap}
.stats b{display:block;font-size:1.7rem}
.stats span{color:var(--muted);font-size:.9rem}
.grid{display:grid;gap:22px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
overflow:hidden;transition:.25s transform,.25s box-shadow;display:flex;flex-direction:column}
.card:hover{transform:translateY(-5px);box-shadow:var(--shadow)}
.card .img{position:relative;aspect-ratio:4/5;overflow:hidden}
.card .img svg{width:100%;height:100%;object-fit:cover}
.badge{position:absolute;top:12px;left:12px;background:var(--fg);color:var(--bg);
font-size:.75rem;font-weight:700;padding:4px 10px;border-radius:999px}
.card .body{padding:16px;display:flex;flex-direction:column;gap:6px;flex:1}
.card h3{font-size:1.05rem}
.price{font-weight:700}
.old{color:var(--muted);text-decoration:line-through;font-weight:400;margin-left:8px;font-size:.9rem}
.card .add{margin-top:auto}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 26px}
.chip{padding:8px 18px;border-radius:999px;border:1px solid var(--line);background:var(--card);
cursor:pointer;font:inherit;color:var(--fg)}
.chip.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.search{width:100%;max-width:360px;padding:12px 18px;border-radius:999px;border:1px solid var(--line);
background:var(--card);color:var(--fg);font:inherit}
.features{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.feature{padding:24px;border-radius:var(--radius);background:var(--card);border:1px solid var(--line)}
.feature .em{font-size:1.8rem}
.steps{counter-reset:s;display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.step{padding:24px;border-radius:var(--radius);border:1px dashed var(--line)}
.step i{font-style:normal;display:inline-grid;place-items:center;width:38px;height:38px;
border-radius:50%;background:var(--accent);color:#fff;font-weight:700;margin-bottom:10px}
.review{padding:22px;border-radius:var(--radius);background:var(--card);border:1px solid var(--line)}
.stars{color:#f5a623;letter-spacing:2px}
details{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin-bottom:10px}
summary{cursor:pointer;font-weight:600}
details p{color:var(--muted);margin-top:8px}
.product{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.product .img{border-radius:24px;overflow:hidden;box-shadow:var(--shadow);aspect-ratio:4/5}
.opts{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 18px}
.crumbs{color:var(--muted);font-size:.9rem;margin-bottom:18px}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.panel{padding:28px;border-radius:var(--radius);background:var(--card);border:1px solid var(--line)}
.panel li{list-style:none;margin:10px 0}
.footer{border-top:1px solid var(--line);padding:40px 0;color:var(--muted);margin-top:40px}
.footer .wrap{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
.drawer{position:fixed;top:0;right:0;height:100%;width:min(400px,100%);background:var(--card);
z-index:100;transform:translateX(100%);transition:.3s transform;padding:22px;display:flex;
flex-direction:column;gap:14px;box-shadow:-10px 0 40px rgba(0,0,0,.25)}
.drawer.open{transform:none}
.drawer .list{flex:1;overflow:auto}
.line{display:flex;justify-content:space-between;gap:10px;padding:10px 0;border-bottom:1px solid var(--line)}
.line button{background:none;border:0;color:var(--accent2);cursor:pointer;font:inherit}
.veil{position:fixed;inset:0;background:rgba(0,0,0,.45);opacity:0;pointer-events:none;
transition:.3s opacity;z-index:90}
.veil.open{opacity:1;pointer-events:auto}
.toast{position:fixed;left:50%;bottom:26px;transform:translate(-50%,120px);background:var(--fg);
color:var(--bg);padding:12px 22px;border-radius:999px;transition:.3s transform;z-index:120}
.toast.show{transform:translate(-50%,0)}
.reveal{opacity:0;transform:translateY(22px);transition:.6s}
.reveal.in{opacity:1;transform:none}
.empty{color:var(--muted);padding:40px 0;text-align:center}
@media(max-width:860px){
.hero-grid,.product,.contact-grid{grid-template-columns:1fr}
.burger{display:inline-block}
.nav{position:absolute;top:68px;left:0;right:0;background:var(--bg);flex-direction:column;
padding:12px 20px;border-bottom:1px solid var(--line);display:none;align-items:stretch}
.nav.open{display:flex}
section{padding:44px 0}}
"""

JS = """
(function(){
  var KEY='neostyle_cart', WA=document.body.dataset.wa || '';
  var cur=document.body.dataset.cur || 'сом';
  var catalog={}; try{catalog=JSON.parse(document.getElementById('catalog-data').textContent)}catch(e){}
  var cart=[];
  try{cart=JSON.parse(localStorage.getItem(KEY)||'[]')}catch(e){cart=[]}
  var $=function(s,r){return (r||document).querySelector(s)};
  var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  var fmt=function(n){return n.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,' ')+' '+cur};
  function save(){try{localStorage.setItem(KEY,JSON.stringify(cart))}catch(e){} render()}
  function toast(t){var el=$('.toast');el.textContent=t;el.classList.add('show');
    clearTimeout(toast.t);toast.t=setTimeout(function(){el.classList.remove('show')},1800)}
  window.addToCart=function(id,opts){
    var p=catalog[id]; if(!p) return;
    cart.push({id:id,opt:opts||''}); save(); toast('Добавлено: '+p.name)};
  function removeAt(i){cart.splice(i,1);save()}
  function render(){
    var c=$('#cart-count'); if(c) c.textContent=cart.length;
    var list=$('#cart-list'), total=$('#cart-total'), wa=$('#cart-wa');
    if(!list) return;
    list.innerHTML=''; var sum=0, lines=[];
    if(!cart.length) list.innerHTML='<p class="empty">Корзина пока пуста</p>';
    cart.forEach(function(it,i){
      var p=catalog[it.id]; if(!p) return; sum+=p.price;
      lines.push((i+1)+'. '+p.name+(it.opt?' ('+it.opt+')':'')+' — '+fmt(p.price));
      var d=document.createElement('div'); d.className='line';
      d.innerHTML='<span>'+p.name+(it.opt?'<br><small>'+it.opt+'</small>':'')+'</span>'+
        '<span>'+fmt(p.price)+' <button aria-label="Удалить">✕</button></span>';
      d.querySelector('button').onclick=function(){removeAt(i)};
      list.appendChild(d)});
    total.textContent=fmt(sum);
    var msg='Здравствуйте! Хочу заказать:\\n'+lines.join('\\n')+'\\nИтого: '+fmt(sum);
    wa.href='https://wa.me/'+WA+'?text='+encodeURIComponent(msg);
    wa.style.display=cart.length?'inline-flex':'none'}
  function drawer(open){$('.drawer').classList.toggle('open',open);$('.veil').classList.toggle('open',open)}
  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-add]');
    if(t){var opt=''; var box=t.closest('[data-product]');
      if(box){var parts=[]; $$('.opts',box).forEach(function(g){
        var on=$('.chip.on',g); if(on) parts.push(on.textContent)}); opt=parts.join(', ')}
      addToCart(t.dataset.add,opt)}
    if(e.target.closest('#open-cart')) drawer(true);
    if(e.target.closest('.veil,#close-cart')) drawer(false);
    var ch=e.target.closest('.opts .chip');
    if(ch){$$('.chip',ch.parentNode).forEach(function(x){x.classList.remove('on')});ch.classList.add('on')}
    if(e.target.closest('.burger')) $('.nav').classList.toggle('open');
    if(e.target.closest('#theme')){
      var d=document.documentElement; var n=d.dataset.theme==='dark'?'light':'dark';
      d.dataset.theme=n; try{localStorage.setItem('neostyle_theme',n)}catch(err){}}});
  // фильтр каталога
  var grid=$('#product-grid');
  if(grid){
    var state={cat:'all',q:''};
    var apply=function(){var shown=0;
      $$('.card',grid).forEach(function(c){
        var ok=(state.cat==='all'||c.dataset.cat===state.cat)&&c.dataset.name.indexOf(state.q)>-1;
        c.style.display=ok?'':'none'; if(ok) shown++});
      $('#no-results').style.display=shown?'none':'block'};
    $$('#filters .chip').forEach(function(b){b.onclick=function(){
      $$('#filters .chip').forEach(function(x){x.classList.remove('on')});b.classList.add('on');
      state.cat=b.dataset.cat;apply()}});
    var s=$('#search'); if(s) s.oninput=function(){state.q=s.value.toLowerCase().trim();apply()};
    var h=location.hash.replace('#','');
    var pre=$('#filters .chip[data-cat="'+h+'"]'); if(pre) pre.click();
  }
  // анимация появления
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(x){
      if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.12});
    $$('.reveal').forEach(function(el){io.observe(el)});
  }else{$$('.reveal').forEach(function(el){el.classList.add('in')})}
  try{var th=localStorage.getItem('neostyle_theme'); if(th) document.documentElement.dataset.theme=th}catch(e){}
  render();
})();
"""
