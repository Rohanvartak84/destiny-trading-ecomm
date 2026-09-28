const catalogChrome = {
  en: {
    home:'Home', about:'About Us', products:'Products', contact:'Contact', quote:'Request a Quote', whatsapp:'WhatsApp',
    chooseLanguage:'Choose language', menuOpen:'Open menu', menuClose:'Close menu', navLabel:'Main navigation',
    brandLabel:'Destiny General Trading LLC — Home', whatsappLabel:'Chat with Destiny on WhatsApp',
    whatsappMessage:'Hello, I would like to enquire about your furniture products.',
    footerDescription:'Furniture for spaces around the world. Based in Dubai, UAE.', footerNavigate:'Navigate',
    footerContact:'Get in touch', footerLocation:'Dubai, United Arab Emirates', footerWhatsApp:'Enquire on WhatsApp ↗',
    footerBottom:'Indoor & outdoor furniture · Dubai, UAE'
  },
  ar: {
    home:'الرئيسية', about:'من نحن', products:'المنتجات', contact:'اتصل بنا', quote:'اطلب عرض سعر', whatsapp:'واتساب',
    chooseLanguage:'اختر اللغة', menuOpen:'افتح القائمة', menuClose:'أغلق القائمة', navLabel:'القائمة الرئيسية',
    brandLabel:'ديستني للتجارة العامة — الرئيسية', whatsappLabel:'تواصل مع ديستني عبر واتساب',
    whatsappMessage:'مرحباً، أود الاستفسار عن منتجات الأثاث لديكم.',
    footerDescription:'أثاث لمساحات حول العالم. مقرنا في دبي، الإمارات العربية المتحدة.', footerNavigate:'روابط سريعة',
    footerContact:'تواصل معنا', footerLocation:'دبي، الإمارات العربية المتحدة', footerWhatsApp:'استفسر عبر واتساب ↗',
    footerBottom:'أثاث داخلي وخارجي · دبي، الإمارات'
  }
};

const WHATSAPP_NUMBER='918140840069';
const root=document.documentElement;
const menu=document.querySelector('.nav');
const menuButton=document.querySelector('.menu-toggle');
const languageMenu=document.querySelector('.language');
const languageButton=document.querySelector('.language-trigger');
const aside=document.querySelector('.catalog-aside');
const asideButton=document.querySelector('[data-aside-toggle]');
const catalogGrid=document.querySelector('[data-catalog-grid]');
const searchInput=document.querySelector('[data-search-input]');
const priceFilter=document.querySelector('[data-price-filter]');
const availabilityFilter=document.querySelector('[data-availability-filter]');
const sortSelect=document.querySelector('[data-sort]');
let visibleCount=8;
let language='en';

function updateCatalogResults(){
  if(!catalogGrid)return;
  const query=(searchInput?.value||'').trim().toLocaleLowerCase();
  const maxPrice=Number(priceFilter?.value||0);
  const stockOnly=Boolean(availabilityFilter?.checked);
  const sort=sortSelect?.value||'featured';
  const cards=Array.from(catalogGrid.querySelectorAll('[data-card]')).sort((a,b)=>{
    if(sort==='featured')return Number(a.dataset.order)-Number(b.dataset.order);
    const first=a.dataset.price===''?Infinity:Number(a.dataset.price);
    const second=b.dataset.price===''?Infinity:Number(b.dataset.price);
    if(!Number.isFinite(first))return Number.isFinite(second)?1:0;
    if(!Number.isFinite(second))return -1;
    return sort==='price-asc' ? first-second : second-first;
  });
  cards.forEach(card=>catalogGrid.append(card));
  let matches=0;
  cards.forEach((card,index)=>{
    const text=(card.dataset[language==='ar'?'searchAr':'searchEn']||'').toLocaleLowerCase();
    const price=card.dataset.price===''?Infinity:Number(card.dataset.price);
    const match=(!query||text.includes(query)) && (!maxPrice||price<=maxPrice) && (!stockOnly||Number(card.dataset.availability)>0);
    if(match){card.hidden=matches>=visibleCount && !query;matches++}else card.hidden=true;
  });
  const count=document.querySelector('[data-results-count]');
  count.textContent=language==='ar'?`عرض ${matches} ${matches===1?'منتج':'منتجات'}`:`${matches} ${matches===1?'product':'products'}`;
  document.querySelector('[data-empty]').hidden=matches!==0;
  const more=document.querySelector('[data-load-more]');
  if(more)more.hidden=Boolean(query)||matches<=visibleCount;
}

function closeMenu(){
  menu.classList.remove('open');
  menuButton.setAttribute('aria-expanded','false');
  menuButton.setAttribute('aria-label',catalogChrome[language].menuOpen);
}
function closeLanguage(){
  languageMenu.classList.remove('open');
  languageButton.setAttribute('aria-expanded','false');
}
function setLanguage(next){
  language=next;
  const chrome=catalogChrome[next];
  root.lang=next;
  root.dir=next==='ar'?'rtl':'ltr';
  document.querySelectorAll('[data-i18n]').forEach(el=>el.textContent=chrome[el.dataset.i18n]);
  document.querySelectorAll('[data-en][data-ar]').forEach(el=>el.textContent=el.dataset[next]);
  document.querySelectorAll('[data-placeholder-en][data-placeholder-ar]').forEach(el=>el.placeholder=el.dataset[next==='ar'?'placeholderAr':'placeholderEn']);
  document.querySelectorAll('[data-alt-en][data-alt-ar]').forEach(el=>el.alt=el.dataset[next==='ar'?'altAr':'altEn']);
  document.querySelectorAll('[data-aria-en][data-aria-ar]').forEach(el=>el.setAttribute('aria-label',el.dataset[next==='ar'?'ariaAr':'ariaEn']));
  document.querySelectorAll('[data-lang]').forEach(el=>{
    const active=el.dataset.lang===next;
    el.classList.toggle('active',active);
    el.setAttribute('aria-pressed',active);
  });
  document.querySelector('.language-current').textContent=next==='ar'?'عربي':'EN';
  languageButton.setAttribute('aria-label',chrome.chooseLanguage);
  document.querySelector('.language-options').setAttribute('aria-label',chrome.chooseLanguage);
  menuButton.setAttribute('aria-label',chrome[menu.classList.contains('open')?'menuClose':'menuOpen']);
  menu.setAttribute('aria-label',chrome.navLabel);
  document.querySelector('.brand').setAttribute('aria-label',chrome.brandLabel);
  document.querySelectorAll('[data-whatsapp]').forEach(el=>{
    el.setAttribute('aria-label',chrome.whatsappLabel);
    el.href=`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(chrome.whatsappMessage)}`;
  });
  const productLink=document.querySelector('[data-product-whatsapp]');
  if(productLink){
    const name=document.body.dataset[next==='ar'?'productNameAr':'productNameEn'];
    const id=document.body.dataset.productId;
    const message=next==='ar'
      ? `مرحباً، أود الاستفسار عن ${name} (رقم المنتج: ${id}). يرجى مشاركة الخيارات المتاحة.`
      : `Hello, I would like to enquire about ${name} (ID: ${id}). Please share the available options.`;
    productLink.href=`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
  }
  document.title=document.body.dataset[next==='ar'?'pageTitleAr':'pageTitleEn'];
  document.querySelector('meta[name="description"]').content=document.body.dataset[next==='ar'?'pageDescriptionAr':'pageDescriptionEn'];
  updateCatalogResults();
  localStorage.setItem('destiny-language',next);
}

languageButton.addEventListener('click',()=>{
  const open=!languageMenu.classList.contains('open');
  languageMenu.classList.toggle('open',open);
  languageButton.setAttribute('aria-expanded',open);
  if(open)closeMenu();
});
document.querySelectorAll('[data-lang]').forEach(el=>el.addEventListener('click',()=>{
  setLanguage(el.dataset.lang);
  closeLanguage();
  languageButton.focus();
}));
document.addEventListener('click',event=>{if(!languageMenu.contains(event.target))closeLanguage()});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){closeLanguage();closeMenu()}});
menuButton.addEventListener('click',()=>{
  closeLanguage();
  const open=!menu.classList.contains('open');
  menu.classList.toggle('open',open);
  menuButton.setAttribute('aria-expanded',open);
  menuButton.setAttribute('aria-label',catalogChrome[language][open?'menuClose':'menuOpen']);
});
document.querySelectorAll('.nav a').forEach(el=>el.addEventListener('click',closeMenu));
asideButton?.addEventListener('click',()=>{
  const open=!aside.classList.contains('is-open');
  aside.classList.toggle('is-open',open);
  asideButton.setAttribute('aria-expanded',open);
});
if(searchInput)searchInput.addEventListener('input',updateCatalogResults);
priceFilter?.addEventListener('change',updateCatalogResults);
availabilityFilter?.addEventListener('change',updateCatalogResults);
sortSelect?.addEventListener('change',updateCatalogResults);
document.querySelectorAll('[data-load-more]').forEach(button=>button.addEventListener('click',()=>{
  visibleCount+=8;
  updateCatalogResults();
}));
document.querySelector('#copyright-year').textContent=new Date().getFullYear();
setLanguage(localStorage.getItem('destiny-language')==='ar'?'ar':'en');
