const copy={
  en:{
    home:'Home',about:'About Us',products:'Products',contact:'Contact',quote:'Request a Quote',whatsapp:'WhatsApp',chooseLanguage:'Choose language',menuOpen:'Open menu',menuClose:'Close menu',navLabel:'Main navigation',brandLabel:'Destiny General Trading LLC — Home',whatsappLabel:'Chat with Destiny on WhatsApp',whatsappMessage:'Hello, I would like to enquire about your furniture products.',
    whoKicker:'Who we are',whoTitle:'Destiny General Trading LLC',whoText:'Based in Dubai, UAE, Destiny General Trading LLC supplies indoor, outdoor, office and custom furniture for buyers internationally.',aboutImageAlt:'Outdoor furniture arranged on a sunlit terrace',
    offerKicker:'What we offer',offerTitle:'Furniture for different spaces.',offerIntro:'Explore our main collections. Tell us about your project, bulk order or custom requirements so we can discuss suitable options.',indoorTitle:'Indoor Furniture',indoorText:'Pieces for living and gathering spaces.',outdoorTitle:'Outdoor Furniture',outdoorText:'Furniture for open-air settings.',officeTitle:'Office Furniture',officeText:'Furnishings for working spaces.',customCategoryTitle:'Custom Furniture',customCategoryText:'Options shaped around your specifications.',
    processKicker:'How we work',processTitle:'From requirements to quotation.',stepOneTitle:'Share your requirements',stepOneText:'Tell us the furniture, quantity and delivery destination you have in mind.',stepTwoTitle:'Discuss the details',stepTwoText:'We discuss suitable products, specifications and any custom needs.',stepThreeTitle:'Receive a quotation',stepThreeText:'We prepare a quotation based on the agreed requirements.',
    valuesTitle:'Why Choose Us?',qualityTitle:'Quality Assurance',qualityText:'Careful material selection and quality checks for lasting performance.',reachTitle:'Global Supply',reachText:'Serving buyers across the Middle East, Africa, Europe, Asia and beyond.',rangeTitle:'Wide Range',rangeText:'Indoor, outdoor, office and custom furniture for different spaces.',customTitle:'Custom Solutions',customText:'Tailored solutions to match your project requirements and style.',supportTitle:'After-Sales Support',supportText:'Support for product-related enquiries after delivery.',
    ctaKicker:'Ready to explore?',ctaTitle:'Tell us what your space needs.',explore:'Explore Products',enquiry:'Send an Enquiry',footerDescription:'Furniture for spaces around the world. Based in Dubai, UAE.',footerNavigate:'Navigate',footerContact:'Get in touch',footerLocation:'Dubai, United Arab Emirates',footerWhatsApp:'Enquire on WhatsApp ↗',footerBottom:'Indoor & outdoor furniture · Dubai, UAE'
  },
  ar:{
    home:'الرئيسية',about:'من نحن',products:'المنتجات',contact:'اتصل بنا',quote:'اطلب عرض سعر',whatsapp:'واتساب',chooseLanguage:'اختر اللغة',menuOpen:'افتح القائمة',menuClose:'أغلق القائمة',navLabel:'القائمة الرئيسية',brandLabel:'ديستني للتجارة العامة — الرئيسية',whatsappLabel:'تواصل مع ديستني عبر واتساب',whatsappMessage:'مرحباً، أود الاستفسار عن منتجات الأثاث لديكم.',
    whoKicker:'من نحن',whoTitle:'ديستني للتجارة العامة ذ.م.م',whoText:'ديستني للتجارة العامة ذ.م.م شركة مقرها دبي، الإمارات العربية المتحدة، وتوفر الأثاث الداخلي والخارجي والمكتبي والمخصص للمشترين حول العالم.',aboutImageAlt:'أثاث خارجي في مساحة مشمسة',
    offerKicker:'ما نقدمه',offerTitle:'أثاث لمساحات متنوعة.',offerIntro:'استكشف مجموعاتنا الرئيسية. أخبرنا عن مشروعك أو طلبك بالجملة أو متطلباتك الخاصة لنناقش الخيارات المناسبة.',indoorTitle:'الأثاث الداخلي',indoorText:'قطع لمساحات المعيشة والتجمع.',outdoorTitle:'الأثاث الخارجي',outdoorText:'أثاث للمساحات المفتوحة.',officeTitle:'أثاث المكاتب',officeText:'تجهيزات لمساحات العمل.',customCategoryTitle:'أثاث حسب الطلب',customCategoryText:'خيارات تلائم المواصفات التي تحتاجها.',
    processKicker:'كيف نعمل',processTitle:'من المتطلبات إلى عرض السعر.',stepOneTitle:'شاركنا متطلباتك',stepOneText:'أخبرنا بنوع الأثاث والكمية ووجهة التسليم التي تفكر فيها.',stepTwoTitle:'نناقش التفاصيل',stepTwoText:'نناقش المنتجات والمواصفات المناسبة وأي احتياجات مخصصة.',stepThreeTitle:'استلم عرض السعر',stepThreeText:'نعد عرض سعر بناءً على المتطلبات المتفق عليها.',
    valuesTitle:'لماذا تختارنا؟',qualityTitle:'ضمان الجودة',qualityText:'نختار المواد بعناية ونتحقق من الجودة لضمان أداء يدوم.',reachTitle:'توريد عالمي',reachText:'نخدم المشترين في الشرق الأوسط وأفريقيا وأوروبا وآسيا وخارجها.',rangeTitle:'تشكيلة متنوعة',rangeText:'أثاث داخلي وخارجي ومكتبي ومخصص لمساحات مختلفة.',customTitle:'حلول مخصصة',customText:'حلول مصممة لتلائم متطلبات مشروعك وأسلوبه.',supportTitle:'دعم ما بعد البيع',supportText:'نساعدك في الاستفسارات المتعلقة بالمنتجات بعد التسليم.',
    ctaKicker:'هل أنت مستعد للاستكشاف؟',ctaTitle:'أخبرنا بما تحتاجه مساحتك.',explore:'تصفح المنتجات',enquiry:'أرسل استفساراً',footerDescription:'أثاث لمساحات حول العالم. مقرنا في دبي، الإمارات العربية المتحدة.',footerNavigate:'روابط سريعة',footerContact:'تواصل معنا',footerLocation:'دبي، الإمارات العربية المتحدة',footerWhatsApp:'استفسر عبر واتساب ↗',footerBottom:'أثاث داخلي وخارجي · دبي، الإمارات'
  }
};
const WHATSAPP_NUMBER='918140840069';
const root=document.documentElement,menu=document.querySelector('.nav'),menuButton=document.querySelector('.menu-toggle'),languageMenu=document.querySelector('.language'),languageButton=document.querySelector('.language-trigger');
let language='en';
function closeMenu(){menu.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label',copy[language].menuOpen)}
function closeLanguage(){languageMenu.classList.remove('open');languageButton.setAttribute('aria-expanded','false')}
function setLanguage(next){
  language=next;root.lang=next;root.dir=next==='ar'?'rtl':'ltr';
  document.querySelectorAll('[data-i18n]').forEach(el=>el.textContent=copy[next][el.dataset.i18n]);
  document.querySelectorAll('[data-i18n-alt]').forEach(el=>el.alt=copy[next][el.dataset.i18nAlt]);
  document.querySelectorAll('[data-lang]').forEach(el=>{const active=el.dataset.lang===next;el.classList.toggle('active',active);el.setAttribute('aria-pressed',active)});
  document.querySelector('.language-current').textContent=next==='ar'?'عربي':'EN';
  languageButton.setAttribute('aria-label',copy[next].chooseLanguage);
  document.querySelector('.language-options').setAttribute('aria-label',copy[next].chooseLanguage);
  menuButton.setAttribute('aria-label',copy[next][menu.classList.contains('open')?'menuClose':'menuOpen']);
  menu.setAttribute('aria-label',copy[next].navLabel);
  document.querySelector('.brand').setAttribute('aria-label',copy[next].brandLabel);
  document.querySelectorAll('[data-whatsapp]').forEach(el=>{el.setAttribute('aria-label',copy[next].whatsappLabel);el.href=`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(copy[next].whatsappMessage)}`});
  document.title=next==='ar'?'من نحن | ديستني للتجارة العامة':'About Destiny General Trading LLC | Furniture Supply from Dubai';
  document.querySelector('meta[name="description"]').content=next==='ar'?'تعرف على ديستني للتجارة العامة، شركة مقرها دبي توفر الأثاث الداخلي والخارجي والمكتبي والمخصص للمشترين حول العالم.':'Learn about Destiny General Trading LLC, a Dubai-based supplier of indoor, outdoor, office and custom furniture for international buyers.';
  localStorage.setItem('destiny-language',next);
}
languageButton.addEventListener('click',()=>{const open=!languageMenu.classList.contains('open');languageMenu.classList.toggle('open',open);languageButton.setAttribute('aria-expanded',open);if(open)closeMenu()});
document.querySelectorAll('[data-lang]').forEach(el=>el.addEventListener('click',()=>{setLanguage(el.dataset.lang);closeLanguage();languageButton.focus()}));
document.addEventListener('click',event=>{if(!languageMenu.contains(event.target))closeLanguage()});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){closeLanguage();closeMenu()}});
menuButton.addEventListener('click',()=>{closeLanguage();const open=!menu.classList.contains('open');menu.classList.toggle('open',open);menuButton.setAttribute('aria-expanded',open);menuButton.setAttribute('aria-label',copy[language][open?'menuClose':'menuOpen'])});
document.querySelectorAll('.nav a').forEach(el=>el.addEventListener('click',closeMenu));
document.querySelector('#copyright-year').textContent=new Date().getFullYear();
setLanguage(localStorage.getItem('destiny-language')==='ar'?'ar':'en');
