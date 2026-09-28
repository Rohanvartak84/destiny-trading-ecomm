const copy = {
  en: {
    home:'Home', about:'About Us', products:'Products', contact:'Contact', quote:'Request a Quote', whatsapp:'WhatsApp', chooseLanguage:'Choose language', menuOpen:'Open menu', menuClose:'Close menu', navLabel:'Main navigation', brandLabel:'Destiny General Trading LLC — Home', pending:'The About Us page is being prepared.', whatsappLabel:'Chat with Destiny on WhatsApp', whatsappMessage:'Hello, I would like to enquire about your furniture products.',
    pageKicker:'Contact us', pageTitle:'Let’s Discuss Your Requirements', pageIntro:'Tell us about the products or bulk order you need, and we’ll help you explore the right options.', contactOptions:'Direct contact', emailTitle:'Email', locationTitle:'Based in Dubai', locationDetail:'Dubai, United Arab Emirates',
    formTitle:'Send an enquiry', formIntro:'Complete the details below. Your enquiry will open in WhatsApp for you to review and send.', nameLabel:'Your name *', companyLabel:'Company name', emailLabel:'Email address *', phoneLabel:'Phone / WhatsApp', countryLabel:'Delivery country *', enquiryTypeLabel:'Enquiry type *', generalEnquiry:'General enquiry', productQuote:'Product quotation', productLabel:'Product name or ID', productPlaceholder:'Optional for a general enquiry', quantityLabel:'Estimated quantity', quantityPlaceholder:'If known', detailsLabel:'Tell us about your requirements *', detailsPlaceholder:'Products, dimensions, materials, timeline or other details', submitEnquiry:'Continue to WhatsApp', formNote:'WhatsApp will open with your enquiry. Tap Send there to deliver it.', reassurance:'Share your requirements and we’ll get back to you with availability and a tailored quotation.', messageTitle:'Enquiry for Destiny General Trading LLC',
    footerDescription:'Furniture for spaces around the world. Based in Dubai, UAE.', footerNavigate:'Navigate', footerContact:'Get in touch', footerLocation:'Dubai, United Arab Emirates', footerWhatsApp:'Enquire on WhatsApp ↗', footerBottom:'Indoor & outdoor furniture · Dubai, UAE'
  },
  ar: {
    home:'الرئيسية', about:'من نحن', products:'المنتجات', contact:'اتصل بنا', quote:'اطلب عرض سعر', whatsapp:'واتساب', chooseLanguage:'اختر اللغة', menuOpen:'افتح القائمة', menuClose:'أغلق القائمة', navLabel:'القائمة الرئيسية', brandLabel:'ديستني للتجارة العامة — الرئيسية', pending:'يجري إعداد صفحة من نحن.', whatsappLabel:'تواصل مع ديستني عبر واتساب', whatsappMessage:'مرحباً، أود الاستفسار عن منتجات الأثاث لديكم.',
    pageKicker:'تواصل معنا', pageTitle:'لنناقش متطلباتك', pageIntro:'أخبرنا بالمنتجات أو طلبية الأثاث بالجملة التي تحتاجها، وسنساعدك في استكشاف الخيارات المناسبة.', contactOptions:'تواصل مباشرة', emailTitle:'البريد الإلكتروني', locationTitle:'مقرنا في دبي', locationDetail:'دبي، الإمارات العربية المتحدة',
    formTitle:'أرسل استفسارك', formIntro:'أكمل التفاصيل أدناه. سيفتح استفسارك في واتساب لتراجعه وترسله.', nameLabel:'الاسم *', companyLabel:'اسم الشركة', emailLabel:'البريد الإلكتروني *', phoneLabel:'الهاتف / واتساب', countryLabel:'بلد التسليم *', enquiryTypeLabel:'نوع الاستفسار *', generalEnquiry:'استفسار عام', productQuote:'طلب عرض سعر لمنتج', productLabel:'اسم المنتج أو رقمه', productPlaceholder:'اختياري للاستفسار العام', quantityLabel:'الكمية التقريبية', quantityPlaceholder:'إذا كانت معروفة', detailsLabel:'أخبرنا بمتطلباتك *', detailsPlaceholder:'المنتجات، المقاسات، المواد، الموعد أو أي تفاصيل أخرى', submitEnquiry:'المتابعة عبر واتساب', formNote:'سيفتح واتساب مع استفسارك. اضغط إرسال هناك لإيصاله.', reassurance:'شاركنا متطلباتك وسنرد عليك بمعلومات التوفر وعرض سعر ملائم لطلبك.', messageTitle:'استفسار إلى ديستني للتجارة العامة',
    footerDescription:'أثاث لمساحات حول العالم. مقرنا في دبي، الإمارات العربية المتحدة.', footerNavigate:'روابط سريعة', footerContact:'تواصل معنا', footerLocation:'دبي، الإمارات العربية المتحدة', footerWhatsApp:'استفسر عبر واتساب ↗', footerBottom:'أثاث داخلي وخارجي · دبي، الإمارات'
  }
};

const WHATSAPP_NUMBER = '918140840069';
const root = document.documentElement;
const menu = document.querySelector('.nav');
const menuButton = document.querySelector('.menu-toggle');
const languageMenu = document.querySelector('.language');
const languageButton = document.querySelector('.language-trigger');
const form = document.querySelector('#contact-form');
const typeField = form.elements.namedItem('type');
const productField = form.elements.namedItem('product');
const productLabel = productField.closest('label').querySelector('span');
const notice = document.querySelector('.notice');
let language = 'en', noticeTimer;

function updateProductRequirement(){
  productField.required = typeField.value === 'product';
  productLabel.textContent = `${copy[language].productLabel}${productField.required ? ' *' : ''}`;
}
function closeMenu(){menu.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label',copy[language].menuOpen)}
function closeLanguage(){languageMenu.classList.remove('open');languageButton.setAttribute('aria-expanded','false')}
function setLanguage(next){
  language=next;root.lang=next;root.dir=next==='ar'?'rtl':'ltr';
  document.querySelectorAll('[data-i18n]').forEach(el=>el.textContent=copy[next][el.dataset.i18n]);
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el=>el.placeholder=copy[next][el.dataset.i18nPlaceholder]);
  document.querySelectorAll('[data-lang]').forEach(el=>{const active=el.dataset.lang===next;el.classList.toggle('active',active);el.setAttribute('aria-pressed',active)});
  document.querySelector('.language-current').textContent=next==='ar'?'عربي':'EN';
  languageButton.setAttribute('aria-label',copy[next].chooseLanguage);
  document.querySelector('.language-options').setAttribute('aria-label',copy[next].chooseLanguage);
  menuButton.setAttribute('aria-label',copy[next][menu.classList.contains('open')?'menuClose':'menuOpen']);
  menu.setAttribute('aria-label',copy[next].navLabel);
  document.querySelector('.brand').setAttribute('aria-label',copy[next].brandLabel);
  document.querySelectorAll('[data-whatsapp]').forEach(el=>{el.setAttribute('aria-label',copy[next].whatsappLabel);el.href=`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(copy[next].whatsappMessage)}`});
  document.title=next==='ar'?'تواصل مع ديستني للتجارة العامة | استفسارات الأثاث':'Contact Destiny General Trading LLC | Furniture Enquiries';
  document.querySelector('meta[name="description"]').content=next==='ar'?'تواصل مع ديستني للتجارة العامة في دبي للاستفسار عن الأثاث الداخلي والخارجي والمكتبي والمخصص.':'Contact Destiny General Trading LLC in Dubai about indoor, outdoor, office and custom furniture enquiries and quotations.';
  if(prefilledProduct){
    const selectedName=next==='ar'&&productAr?productAr:product;
    const idLabel=next==='ar'?'رقم المنتج':'ID';
    productField.value=selectedName&&productId?`${selectedName} (${idLabel}: ${productId})`:selectedName||productId;
  }
  updateProductRequirement();
  localStorage.setItem('destiny-language',next);
}

const params=new URLSearchParams(window.location.search);
const product=(params.get('product')||'').trim().slice(0,120);
const productAr=(params.get('productAr')||'').trim().slice(0,120);
const productId=(params.get('id')||params.get('productId')||'').trim().slice(0,40);
let prefilledProduct=Boolean(product||productId);
if(product||productId){
  typeField.value='product';
  productField.value=product&&productId?`${product} (ID: ${productId})`:product||productId;
}
productField.addEventListener('input',()=>{prefilledProduct=false});
typeField.addEventListener('change',updateProductRequirement);
languageButton.addEventListener('click',()=>{const open=!languageMenu.classList.contains('open');languageMenu.classList.toggle('open',open);languageButton.setAttribute('aria-expanded',open);if(open)closeMenu()});
document.querySelectorAll('[data-lang]').forEach(el=>el.addEventListener('click',()=>{setLanguage(el.dataset.lang);closeLanguage();languageButton.focus()}));
document.addEventListener('click',event=>{if(!languageMenu.contains(event.target))closeLanguage()});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){closeLanguage();closeMenu()}});
menuButton.addEventListener('click',()=>{closeLanguage();const open=!menu.classList.contains('open');menu.classList.toggle('open',open);menuButton.setAttribute('aria-expanded',open);menuButton.setAttribute('aria-label',copy[language][open?'menuClose':'menuOpen'])});
document.querySelectorAll('.nav a').forEach(el=>el.addEventListener('click',()=>closeMenu()));
document.querySelectorAll('[data-pending]').forEach(el=>el.addEventListener('click',event=>{event.preventDefault();notice.textContent=copy[language].pending;notice.classList.add('show');clearTimeout(noticeTimer);noticeTimer=setTimeout(()=>notice.classList.remove('show'),4000)}));
document.querySelector('#copyright-year').textContent=new Date().getFullYear();
setLanguage(localStorage.getItem('destiny-language')==='ar'?'ar':'en');

form.addEventListener('submit',event=>{
  event.preventDefault();
  const data=new FormData(form);
  const label=key=>copy[language][key].replace(/\s*\*$/,'');
  const line=(key,value)=>`${label(key)}: ${String(value).trim()}`;
  const parts=[copy[language].messageTitle,
    line('nameLabel',data.get('name')),
    data.get('company')?line('companyLabel',data.get('company')):null,
    line('emailLabel',data.get('email')),
    data.get('phone')?line('phoneLabel',data.get('phone')):null,
    line('countryLabel',data.get('country')),
    line('enquiryTypeLabel',copy[language][data.get('type')==='product'?'productQuote':'generalEnquiry']),
    data.get('product')?line('productLabel',data.get('product')):null,
    data.get('quantity')?line('quantityLabel',data.get('quantity')):null,
    '',String(data.get('details')).trim()
  ];
  window.location.assign(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(parts.filter(item=>item!==null).join('\n'))}`);
});
