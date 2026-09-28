"""Generate static, bilingual catalogue pages from catalog/products.json."""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DATA = json.loads((ROOT / "catalog/products.json").read_text())
SHIPPING = json.loads((ROOT / "catalog/shipping.json").read_text())
CATEGORIES = {item["slug"]: item for item in DATA["categories"]}
PRODUCTS = DATA["products"]
TEMPLATE = (DIST / "about.html").read_text()
HEADER = TEMPLATE[:TEMPLATE.index("  <main>")]
FOOTER = TEMPLATE[TEMPLATE.index('  <footer class="site-footer">'):]
FOOTER = FOOTER.replace('<script src="./about.js" defer></script>', '<script src="./catalog.js" defer></script>')


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def localized(tag: str, value: dict, **attrs: str) -> str:
    attributes = " ".join(f'{key.removesuffix("_").replace("_", "-")}="{esc(val)}"' for key, val in attrs.items())
    return f'<{tag} data-en="{esc(value["en"])}" data-ar="{esc(value["ar"])}" {attributes}>{esc(value["en"])}</{tag}>'


def image(image_name: str, alt: dict, *, kind: str, eager: bool = False) -> str:
    base = image_name.removesuffix(".webp")
    if base.startswith("product-"):
        original_width,scaled_height=900,675
        srcset=f'./{base}-480.webp 480w, ./{base}.webp 900w'
        src=f'./{base}.webp'
    else:
        original_width = 1536 if base in ("category-office", "category-custom") else 1448
        scaled_height = 600 if original_width == 1536 else 675
        srcset = f'./{base}-480.webp 480w, ./{base}-900.webp 900w, ./{base}.webp {original_width}w'
        src=f'./{base}-900.webp'
    sizes = "(min-width: 1100px) 25vw, (min-width: 690px) 50vw, 100vw" if kind == "card" else "(min-width: 900px) 54vw, 100vw"
    priority = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    return (f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{esc(alt["en"])}" data-alt-en="{esc(alt["en"])}" data-alt-ar="{esc(alt["ar"])}" '
            f'width="900" height="{scaled_height}" {priority} decoding="async">')


def product_card(product: dict, *, eager: bool = False, hidden: bool = False) -> str:
    category = CATEGORIES[product["category"]]
    title = localized("h3", product["name"])
    description = localized("p", product["description"])
    link = f'./product-{product["slug"]}.html'
    search_en=f'{product["name"]["en"]} {product["description"]["en"]} {product["id"]}'
    search_ar=f'{product["name"]["ar"]} {product["description"]["ar"]} {product["id"]}'
    price = product["price_aed_incl_vat"]
    commerce = (f'<div class="shop-card-price"><strong>AED {price:,.0f}</strong><span data-en="Demo price · VAT included" data-ar="سعر تجريبي · شامل ضريبة القيمة المضافة">Demo price · VAT included</span></div>'
                f'<button class="shop-add" type="button" data-add-to-cart="{esc(product["id"])}" data-en="Add to cart" data-ar="أضف إلى السلة">Add to cart</button>') if price is not None else (
                '<p class="shop-custom-note" data-en="Made to your requirements · Price on request" data-ar="حسب متطلباتك · السعر عند الطلب">Made to your requirements · Price on request</p>')
    availability = (f'<span class="shop-availability" data-en="Demo stock: {product["demo_stock"]} available" data-ar="مخزون تجريبي: {product["demo_stock"]} متاح">Demo stock: {product["demo_stock"]} available</span>'
                    if price is not None else '<span class="shop-availability" data-en="Availability on enquiry" data-ar="التوفر عند الاستفسار">Availability on enquiry</span>')
    return (f'<article class="catalog-product-card"{" hidden" if hidden else ""} data-card '
            f'data-search-en="{esc(search_en)}" data-search-ar="{esc(search_ar)}" data-order="{PRODUCTS.index(product)}" data-price="{price if price is not None else ""}" data-availability="{product["demo_stock"] if price is not None else 0}"><a class="catalog-product-image" href="{link}" '
            f'aria-label="View {esc(product["name"]["en"])} details" '
            f'data-aria-en="View {esc(product["name"]["en"])} details" '
            f'data-aria-ar="عرض تفاصيل {esc(product["name"]["ar"])}">'
            + image(product["image"], product["alt"], kind="card", eager=eager)
            + '</a><div class="catalog-product-copy">'
            + localized("span", category["name"], class_="catalog-product-category")
            + f'{title}{description}{availability}{commerce}<a class="catalog-detail-link" href="{link}" '
            + f'data-en="View Details" data-ar="عرض التفاصيل">View Details <span aria-hidden="true">↗</span></a>'
            + '</div></article>')


def product_grid(products: list[dict], *, eager_first: bool = False) -> str:
    cards = ''.join(product_card(p, eager=eager_first and i == 0, hidden=i >= 8)
                    for i, p in enumerate(products))
    more = ('<button class="catalog-load-more" type="button" data-load-more data-en="Load More" '
            'data-ar="عرض المزيد">Load More</button>') if len(products) > 8 else ''
    return f'<div class="catalog-product-grid" data-catalog-grid>{cards}</div>{more}'


def related_products(product: dict, limit: int = 3) -> list[dict]:
    same=[p for p in PRODUCTS if p['id'] != product['id'] and p['category'] == product['category']]
    other=[p for p in PRODUCTS if p['id'] != product['id'] and p['category'] != product['category']]
    return (same+other)[:limit]


def sidebar(current: str = "", *, product: dict | None = None) -> str:
    heading={"en": "Browse furniture" if product else "Filter products",
             "ar": "تصفح الأثاث" if product else "تصفية المنتجات"}
    all_link = ('<a href="./products.html" ' + ('aria-current="page" ' if not current and not product else '')
                + f'><span data-en="All Products" data-ar="كل المنتجات">All Products</span><span>{len(PRODUCTS)}</span></a>')
    links = ''.join(
        f'<a href="./category-{c["slug"]}.html" '
        + ('aria-current="page" ' if current == c["slug"] else '')
        + '>'
        + localized('span', c['name'])
        + f'<span>{sum(p["category"] == c["slug"] for p in PRODUCTS)}</span></a>'
        for c in DATA['categories']
    )
    search = ('<div class="catalog-filter-search"><label for="catalog-search" data-en="Search products" '
              'data-ar="ابحث عن منتج">Search products</label><input id="catalog-search" type="search" '
              'data-search-input data-placeholder-en="Name or product ID" data-placeholder-ar="الاسم أو رقم المنتج" '
              'placeholder="Name or product ID" autocomplete="off"></div>'
              '<div class="shop-filters"><label for="price-filter" data-en="Maximum price" data-ar="الحد الأقصى للسعر">Maximum price</label>'
              '<select id="price-filter" data-price-filter><option value="" data-en="Any price" data-ar="أي سعر">Any price</option>'
              '<option value="1000" data-en="Up to AED 1,000" data-ar="حتى ١٬٠٠٠ درهم">Up to AED 1,000</option>'
              '<option value="2500" data-en="Up to AED 2,500" data-ar="حتى ٢٬٥٠٠ درهم">Up to AED 2,500</option>'
              '<option value="5000" data-en="Up to AED 5,000" data-ar="حتى ٥٬٠٠٠ درهم">Up to AED 5,000</option></select>'
              '<label class="shop-check"><input type="checkbox" data-availability-filter> <span data-en="Demo in stock only" data-ar="المتوفر تجريبياً فقط">Demo in stock only</span></label></div>') if not product else ''
    other = related_products(product) if product else []
    more = ('<div class="catalog-aside-more"><h3 data-en="More products" data-ar="منتجات أخرى">More products</h3>'
            + ''.join(f'<a href="./product-{p["slug"]}.html"><img src="./{p["image"].removesuffix(".webp")}-480.webp" '
                      f'alt="" width="64" height="64" loading="lazy">{localized("span", p["name"])}</a>' for p in other)
            + '</div>') if other else ''
    return ('<aside class="catalog-aside"><button class="catalog-aside-toggle" type="button" aria-expanded="false" '
            'aria-controls="catalog-aside-content" data-aside-toggle>'
            + localized('span', heading) + '<span aria-hidden="true">⌄</span></button>'
            + '<div class="catalog-aside-content" id="catalog-aside-content">'
            + localized('h2', heading) + search
            + '<nav class="catalog-filter-links" aria-label="Furniture categories" '
            'data-aria-en="Furniture categories" data-aria-ar="فئات الأثاث">'
            + all_link + links + '</nav>' + more + '</div></aside>')


def page(main: str, *, title: dict, description: dict, active: bool = True, product: dict | None = None) -> str:
    top = HEADER.replace('<title>About Destiny General Trading LLC | Furniture Supply from Dubai</title>',
                         f'<title>{esc(title["en"])}</title>')
    top = top.replace('Learn about Destiny General Trading LLC, a Dubai-based supplier of indoor, outdoor, office and custom furniture for international buyers.', esc(description["en"]))
    top = top.replace('href="./about.html" aria-current="page"', 'href="./about.html"')
    top = top.replace('href="./index.html#products"', 'href="./products.html"')
    top = top.replace('href="./contact.html" data-i18n="quote"', 'href="./contact.html" data-i18n="quote"')
    if active:
        top = top.replace('href="./products.html" data-i18n="products"', 'href="./products.html" aria-current="page" data-i18n="products"')
    top = top.replace('<body>', f'<body data-page-title-en="{esc(title["en"])}" data-page-title-ar="{esc(title["ar"])}" data-page-description-en="{esc(description["en"])}" data-page-description-ar="{esc(description["ar"])}"'
                      + (f' data-product-name-en="{esc(product["name"]["en"])}" data-product-name-ar="{esc(product["name"]["ar"])}" data-product-id="{esc(product["id"])}"' if product else '') + '>')
    bottom = FOOTER.replace('href="./index.html#products"', 'href="./products.html"')
    return top + f'  <main>{main}</main>\n' + bottom


def build_overview() -> None:
    title = {"en": "Furniture Products | Destiny General Trading LLC", "ar": "منتجات الأثاث | ديستني للتجارة العامة"}
    desc = {"en": "Explore indoor, outdoor, office and custom furniture at Destiny General Trading LLC. Enquire about available options and quotations.",
            "ar": "تصفح الأثاث الداخلي والخارجي والمكتبي والمخصص لدى ديستني للتجارة العامة، واستفسر عن الخيارات المتاحة وعروض الأسعار."}
    main = ('<section class="catalog-page catalog-shell"><div class="catalog-layout">'
            + sidebar() + '<div class="catalog-content"><div class="catalog-page-heading">'
            + '<p class="collections-kicker" data-en="Furniture catalogue" data-ar="كتالوج الأثاث">Furniture catalogue</p>'
            + '<h1 data-en="All Products" data-ar="كل المنتجات">All Products</h1>'
            + f'</div><p class="shop-demo-note" data-en="Sample products and prices for preview. AED prices include illustrative UAE VAT; delivery estimates appear in the cart." data-ar="منتجات وأسعار تجريبية للمعاينة. الأسعار بالدرهم تشمل ضريبة قيمة مضافة إماراتية توضيحية؛ تظهر تقديرات التوصيل في السلة.">Sample products and prices for preview. AED prices include illustrative UAE VAT; delivery estimates appear in the cart.</p><div class="shop-list-toolbar"><p class="catalog-results-count" data-results-count>{len(PRODUCTS)} products</p><label><span data-en="Sort" data-ar="ترتيب">Sort</span><select data-sort><option value="featured" data-en="Featured" data-ar="المميزة">Featured</option><option value="price-asc" data-en="Price: low to high" data-ar="السعر: من الأقل إلى الأعلى">Price: low to high</option><option value="price-desc" data-en="Price: high to low" data-ar="السعر: من الأعلى إلى الأقل">Price: high to low</option></select></label></div>'
            + product_grid(PRODUCTS, eager_first=True)
            + '<p class="catalog-empty" hidden data-empty data-en="No products match your search." data-ar="لا توجد منتجات تطابق بحثك.">No products match your search.</p>'
            + '</div></div></section>')
    (DIST / "products.html").write_text(page(main, title=title, description=desc))


def build_category(category: dict) -> None:
    products = [p for p in PRODUCTS if p["category"] == category["slug"]]
    title = {lang: f'{category["name"][lang]} | Destiny General Trading LLC' for lang in ("en", "ar")}
    desc = {"en": f'Browse {category["name"]["en"].lower()} and enquire with Destiny General Trading LLC in Dubai.',
            "ar": f'تصفح {category["name"]["ar"]} واستفسر من ديستني للتجارة العامة في دبي.'}
    main = ('<section class="catalog-page catalog-shell"><div class="catalog-layout">'
            + sidebar(category["slug"]) + '<div class="catalog-content"><div class="catalog-page-heading">'
            + '<p class="catalog-breadcrumb"><a href="./products.html" data-en="Products" data-ar="المنتجات">Products</a><span aria-hidden="true"> / </span>'
            + localized("span", category["name"]) + '</p>'
            + localized("h1", category["name"]) + localized("p", category["intro"], class_="catalog-intro-text")
            + f'</div><p class="shop-demo-note" data-en="Sample catalogue. Displayed AED prices include illustrative UAE VAT; custom furniture is quoted individually." data-ar="كتالوج تجريبي. الأسعار المعروضة بالدرهم تشمل ضريبة قيمة مضافة إماراتية توضيحية؛ يُسعّر الأثاث حسب الطلب بشكل منفصل.">Sample catalogue. Displayed AED prices include illustrative UAE VAT; custom furniture is quoted individually.</p><div class="shop-list-toolbar"><p class="catalog-results-count" data-results-count>{len(products)} {"product" if len(products)==1 else "products"}</p><label><span data-en="Sort" data-ar="ترتيب">Sort</span><select data-sort><option value="featured" data-en="Featured" data-ar="المميزة">Featured</option><option value="price-asc" data-en="Price: low to high" data-ar="السعر: من الأقل إلى الأعلى">Price: low to high</option><option value="price-desc" data-en="Price: high to low" data-ar="السعر: من الأعلى إلى الأقل">Price: high to low</option></select></label></div>'
            + product_grid(products, eager_first=True)
            + '<p class="catalog-empty" hidden data-empty data-en="No products match your search." data-ar="لا توجد منتجات تطابق بحثك.">No products match your search.</p>'
            + '</div></div></section>')
    (DIST / f'category-{category["slug"]}.html').write_text(page(main, title=title, description=desc))


def build_product(product: dict) -> None:
    category = CATEGORIES[product["category"]]
    title = {lang: f'{product["name"][lang]} | Destiny General Trading LLC' for lang in ("en", "ar")}
    desc = {"en": f'Explore {product["name"]["en"].lower()}, demo specifications and related furniture. Request a tailored quote from Destiny General Trading LLC.',
            "ar": f'تصفح {product["name"]["ar"]} والمواصفات التجريبية والأثاث ذي الصلة. اطلب عرض سعر من ديستني للتجارة العامة.'}
    quote = './contact.html?' + urlencode({"product": product["name"]["en"], "productAr": product["name"]["ar"], "id": product["id"]}) + '#contact-form'
    whatsapp = 'https://wa.me/918140840069?' + urlencode({"text": f'Hello, I would like to enquire about {product["name"]["en"]} (ID: {product["id"]}). Please share the available options.'})
    related = related_products(product)
    specs = product["specifications"]
    price = product["price_aed_incl_vat"]
    options = product.get('demo_options', {})
    def option_select(kind: str, label_en: str, label_ar: str) -> str:
        values = options[kind]
        choices = ''
        for value in values:
            delta = value['price_delta_aed']
            en = value['name']['en'] + (f' (+AED {delta})' if delta else '')
            ar = value['name']['ar'] + (f' (+{delta} درهم)' if delta else '')
            choices += f'<option value="{esc(value["code"])}" data-en="{esc(en)}" data-ar="{esc(ar)}">{esc(en)}</option>'
        return f'<label><span data-en="{label_en}" data-ar="{label_ar}">{label_en}</span><select data-product-option="{kind}">{choices}</select></label>'
    primary_action = (f'<p class="shop-availability" data-en="Demo stock: {product["demo_stock"]} available" data-ar="مخزون تجريبي: {product["demo_stock"]} متاح">Demo stock: {product["demo_stock"]} available</p>'
                      f'<div class="shop-detail-price"><strong data-product-price>AED {price:,.0f}</strong><span data-en="Demo item price · VAT included" data-ar="سعر تجريبي للمنتج · شامل الضريبة">Demo item price · VAT included</span></div>'
                      '<div class="shop-product-options">'
                      + option_select('size','Size','المقاس') + option_select('finish','Finish','التشطيب')
                      + '<label><span data-en="Quantity" data-ar="الكمية">Quantity</span><input type="number" data-product-quantity min="1" max="99" value="1" step="1"></label></div>'
                      f'<button class="catalog-quote-button shop-detail-add" type="button" data-add-to-cart="{esc(product["id"])}" data-en="Add to cart" data-ar="أضف إلى السلة">Add to cart</button>') if price is not None else (
                      '<p class="shop-custom-note" data-en="Custom piece · Price on request" data-ar="قطعة حسب الطلب · السعر عند الطلب">Custom piece · Price on request</p>'
                      f'<a class="catalog-quote-button" href="{esc(quote)}" data-en="Request a Quote" data-ar="اطلب عرض سعر">Request a Quote</a>')
    if specs:
        spec_content = '<dl class="catalog-spec-list">' + ''.join(
            f'<div><dt data-en="{esc(item["label"]["en"])}" data-ar="{esc(item["label"]["ar"])}">{esc(item["label"]["en"])}</dt>'
            f'<dd data-en="{esc(item["value"]["en"])}" data-ar="{esc(item["value"]["ar"])}">{esc(item["value"]["en"])}</dd></div>'
            for item in specs
        ) + '</dl>'
    else:
        spec_content = '<p data-en="Ask about available options." data-ar="استفسر عن الخيارات المتاحة.">Ask about available options.</p>'
    main = ('<section class="catalog-page catalog-shell"><div class="catalog-layout catalog-layout-detail">'
            + sidebar(category["slug"],product=product) + '<div class="catalog-content"><div class="catalog-detail">'
            + '<p class="catalog-breadcrumb"><a href="./products.html" data-en="Products" data-ar="المنتجات">Products</a><span aria-hidden="true"> / </span>'
            + f'<a href="./category-{category["slug"]}.html" data-en="{esc(category["name"]["en"])}" data-ar="{esc(category["name"]["ar"])}">{esc(category["name"]["en"])}</a></p>'
            + '<div class="catalog-detail-layout"><div class="catalog-detail-head">'
            + localized("span", category["name"], class_="catalog-product-category")
            + localized("h1", product["name"])
            + f'<p class="catalog-product-id" data-en="ID: {esc(product["id"])}" data-ar="رقم المنتج: {esc(product["id"])}">ID: {esc(product["id"])}</p>'
            + primary_action
            + '</div><div class="catalog-detail-image">'
            + image(product["images"][0]["file"], product["images"][0]["alt"], kind="detail", eager=True)
            + (('<div class="shop-gallery-thumbs">' + ''.join(f'<button type="button" aria-label="View photo {index+1}" data-aria-en="View photo {index+1}" data-aria-ar="عرض الصورة {index+1}" data-gallery-image="./{esc(item["file"])}" data-gallery-alt-en="{esc(item["alt"]["en"])}" data-gallery-alt-ar="{esc(item["alt"]["ar"])}"><img src="./{esc(item["file"].removesuffix(".webp"))}-480.webp" alt="" width="75" height="75" loading="lazy"></button>' for index,item in enumerate(product['images'])) + '</div>') if len(product['images'])>1 else '')
            + '</div><div class="catalog-detail-more">'
            + localized("p", product["description"], class_="catalog-detail-description")
            + (f'<p class="shop-demo-note" data-en="Illustrative item price includes UAE VAT. Select a destination in the cart to see a demo shipping estimate and order total." data-ar="سعر المنتج التوضيحي يشمل الضريبة الإماراتية. اختر وجهة التوصيل في السلة لمعرفة تقدير الشحن والمجموع التجريبي.">Illustrative item price includes UAE VAT. Select a destination in the cart to see a demo shipping estimate and order total.</p>' if price is not None else '')
            + '<section class="catalog-specifications" aria-labelledby="catalog-spec-title">'
            + '<h2 id="catalog-spec-title" data-en="Demo Specifications" data-ar="مواصفات تجريبية">Demo Specifications</h2>'
            + spec_content + '</section>'
            + (f'<form class="shop-custom-form" data-custom-enquiry data-product-id="{esc(product["id"])}" data-product-name-en="{esc(product["name"]["en"])}" data-product-name-ar="{esc(product["name"]["ar"])}"><h2 data-en="Enquire about this custom piece" data-ar="استفسر عن هذه القطعة حسب الطلب">Enquire about this custom piece</h2><label><span data-en="Your name" data-ar="اسمك">Your name</span><input name="name" required maxlength="100" autocomplete="name"></label><label><span data-en="Email address" data-ar="البريد الإلكتروني">Email address</span><input name="email" type="email" required maxlength="150" autocomplete="email"></label><label><span data-en="Delivery country" data-ar="بلد التوصيل">Delivery country</span><input name="country" required maxlength="100" autocomplete="country-name"></label><label><span data-en="Requirements" data-ar="المتطلبات">Requirements</span><textarea name="details" required maxlength="2000" rows="4"></textarea></label><button type="submit" data-en="Continue to WhatsApp" data-ar="المتابعة عبر واتساب">Continue to WhatsApp</button><p data-en="Your message opens in WhatsApp for review; send it there to reach us." data-ar="ستفتح الرسالة في واتساب للمراجعة؛ أرسلها هناك للتواصل معنا.">Your message opens in WhatsApp for review; send it there to reach us.</p></form>' if price is None else '')
            + '</div></div></div><section class="catalog-related" aria-labelledby="catalog-related-title">'
            + '<h2 id="catalog-related-title" data-en="Explore more examples" data-ar="استكشف أمثلة أخرى">Explore more examples</h2><div class="catalog-product-grid">'
            + ''.join(product_card(p) for p in related) + '</div></section></div></div></section>')
    (DIST / f'product-{product["slug"]}.html').write_text(page(main, title=title, description=desc, product=product))


def build_cart() -> None:
    title = {"en": "Your Cart | Destiny Furniture Shop Demo", "ar": "سلة التسوق | متجر ديستني التجريبي"}
    desc = {"en": "Review your furniture selections and an estimated destination-based total before guest checkout.",
            "ar": "راجع اختيارات الأثاث والمجموع المقدر حسب وجهة التوصيل قبل إتمام الطلب كضيف."}
    main = ('<section class="shop-cart-page catalog-shell" data-cart-page>'
            '<p class="collections-kicker" data-shop-en="Furniture shop demo" data-shop-ar="متجر الأثاث التجريبي">Furniture shop demo</p>'
            '<h1 data-shop-en="Your cart" data-shop-ar="سلة التسوق">Your cart</h1>'
            '<p class="shop-demo-note" data-shop-en="Demo prices in AED include illustrative 5% UAE VAT. Choose your destination to include estimated shipping in the total. Actual freight and import charges need confirmation." data-shop-ar="الأسعار التجريبية بالدرهم تشمل ضريبة قيمة مضافة إماراتية توضيحية بنسبة ٥٪. اختر وجهتك لإضافة تقدير الشحن إلى المجموع. يجب تأكيد الشحن الفعلي ورسوم الاستيراد.">Demo prices in AED include illustrative 5% UAE VAT. Choose your destination to include estimated shipping in the total. Actual freight and import charges need confirmation.</p>'
            '<div class="shop-cart-layout"><div class="shop-cart-items" data-cart-items></div>'
            '<aside class="shop-cart-summary"><h2 data-shop-en="Order summary" data-shop-ar="ملخص الطلب">Order summary</h2>'
            '<label class="shop-shipping-field"><span data-shop-en="Delivery country" data-shop-ar="بلد التوصيل">Delivery country</span><select data-shipping-country>' + shipping_options() + '</select></label>'
            '<label class="shop-shipping-field"><span data-shop-en="Shipping method" data-shop-ar="طريقة الشحن">Shipping method</span><select data-shipping-method><option value="standard" data-shop-en="Standard delivery" data-shop-ar="توصيل عادي">Standard delivery</option><option value="express" data-shop-en="Express delivery" data-shop-ar="توصيل سريع">Express delivery</option></select></label>'
            '<div class="shop-summary-row"><span data-shop-en="Items" data-shop-ar="القطع">Items</span><strong data-cart-count-text>0</strong></div>'
            '<div class="shop-summary-row"><span data-shop-en="Included demo VAT (5%)" data-shop-ar="الضريبة التجريبية المشمولة (٥٪)">Included demo VAT (5%)</span><strong data-cart-vat>AED 0</strong></div>'
            '<div class="shop-summary-row"><span data-shop-en="Estimated shipping" data-shop-ar="الشحن المقدر">Estimated shipping</span><strong data-cart-shipping>AED 120</strong></div>'
            '<div class="shop-summary-row shop-summary-total"><span data-shop-en="Estimated total incl. shipping" data-shop-ar="المجموع المقدر شامل الشحن">Estimated total incl. shipping</span><strong data-cart-total>AED 0</strong></div>'
            '<p data-shop-en="Demo rates only. Destination duties and any additional taxes are not included." data-shop-ar="أسعار تجريبية فقط. الرسوم الجمركية وأي ضرائب إضافية في الوجهة غير مشمولة.">Demo rates only. Destination duties and any additional taxes are not included.</p>'
            '<a class="shop-cart-send" data-checkout-link href="./checkout.html" data-shop-en="Continue to guest checkout" data-shop-ar="المتابعة كضيف لإتمام الطلب">Continue to guest checkout</a>'
            '<p class="shop-send-note" data-shop-en="No payment is collected in this demo." data-shop-ar="لا تُحصّل مدفوعات في هذا العرض التجريبي.">No payment is collected in this demo.</p></aside></div></section>')
    (DIST / 'cart.html').write_text(page(main, title=title, description=desc, active=False))


def shipping_options() -> str:
    options = ''.join(f'<option value="{esc(country["code"])}" data-shop-en="{esc(country["name"]["en"])}" data-shop-ar="{esc(country["name"]["ar"])}">{esc(country["name"]["en"])}</option>' for country in SHIPPING['countries'])
    return options + '<option value="OTHER" data-shop-en="Other country — ask for a quote" data-shop-ar="بلد آخر — اطلب عرض شحن">Other country — ask for a quote</option>'


def build_checkout() -> None:
    title = {"en": "Guest Checkout | Destiny Furniture Shop Demo", "ar": "إتمام الطلب كضيف | متجر ديستني التجريبي"}
    desc = {"en": "Enter delivery details and review a sample shipping-inclusive total for your furniture selections.",
            "ar": "أدخل تفاصيل التوصيل وراجع المجموع التجريبي الشامل للشحن لاختياراتك من الأثاث."}
    main = ('<section class="shop-cart-page catalog-shell" data-checkout-page><p class="collections-kicker" data-shop-en="Guest checkout · demo" data-shop-ar="إتمام الطلب كضيف · تجريبي">Guest checkout · demo</p>'
            '<h1 data-shop-en="Delivery & checkout" data-shop-ar="التوصيل وإتمام الطلب">Delivery & checkout</h1>'
            '<p class="shop-demo-note" data-shop-en="This is a checkout preview. No payment or actual order is submitted, and no email is sent. The total includes demo item VAT and estimated shipping for the selected country." data-shop-ar="هذه معاينة لإتمام الطلب. لا تُحصّل مدفوعات ولا يُنفّذ طلب فعلي ولا يُرسل بريد إلكتروني. يشمل المجموع ضريبة المنتجات التجريبية وتقدير الشحن إلى البلد المحدد.">This is a checkout preview. No payment or actual order is submitted, and no email is sent. The total includes demo item VAT and estimated shipping for the selected country.</p>'
            '<div class="shop-cart-layout"><form class="shop-checkout-form" data-checkout-form><h2 data-shop-en="Contact & delivery" data-shop-ar="التواصل والتوصيل">Contact & delivery</h2>'
            '<div class="shop-form-grid">'
            '<label><span data-shop-en="Full name *" data-shop-ar="الاسم الكامل *">Full name *</span><input name="name" required autocomplete="name" maxlength="100"></label>'
            '<label><span data-shop-en="Email address *" data-shop-ar="البريد الإلكتروني *">Email address *</span><input name="email" type="email" required autocomplete="email" maxlength="150"></label>'
            '<label><span data-shop-en="Phone *" data-shop-ar="رقم الهاتف *">Phone *</span><input name="phone" type="tel" required autocomplete="tel" maxlength="40"></label>'
            '<label><span data-shop-en="Delivery country *" data-shop-ar="بلد التوصيل *">Delivery country *</span><select name="country" data-shipping-country required>' + shipping_options() + '</select></label>'
            '<label class="shop-wide"><span data-shop-en="Street address *" data-shop-ar="العنوان *">Street address *</span><input name="address" required autocomplete="street-address" maxlength="180"></label>'
            '<label><span data-shop-en="City *" data-shop-ar="المدينة *">City *</span><input name="city" required autocomplete="address-level2" maxlength="100"></label>'
            '<label><span data-shop-en="Postal code" data-shop-ar="الرمز البريدي">Postal code</span><input name="postal" autocomplete="postal-code" maxlength="30"></label>'
            '<label><span data-shop-en="Shipping method" data-shop-ar="طريقة الشحن">Shipping method</span><select name="method" data-shipping-method><option value="standard" data-shop-en="Standard delivery" data-shop-ar="توصيل عادي">Standard delivery</option><option value="express" data-shop-en="Express delivery" data-shop-ar="توصيل سريع">Express delivery</option></select></label>'
            '<label><span data-shop-en="Payment method (demo)" data-shop-ar="طريقة الدفع (تجريبية)">Payment method (demo)</span><select name="payment"><option value="card" data-shop-en="Card — demonstration only" data-shop-ar="بطاقة — للعرض فقط">Card — demonstration only</option><option value="bank" data-shop-en="Bank transfer — demonstration only" data-shop-ar="تحويل بنكي — للعرض فقط">Bank transfer — demonstration only</option></select></label>'
            '<label class="shop-wide"><span data-shop-en="Delivery notes" data-shop-ar="ملاحظات التوصيل">Delivery notes</span><textarea name="notes" rows="3" maxlength="500"></textarea></label></div>'
            '<p class="shop-checkout-hint" data-shop-en="No card number is requested. Your contact and address details stay in this browser during this demo and are not submitted." data-shop-ar="لا نطلب رقم البطاقة. تبقى بيانات التواصل والعنوان في هذا المتصفح خلال العرض التجريبي ولا تُرسل.">No card number is requested. Your contact and address details stay in this browser during this demo and are not submitted.</p>'
            '<button class="shop-cart-send" type="submit" data-shop-en="Create demo order preview" data-shop-ar="إنشاء معاينة طلب تجريبي">Create demo order preview</button></form>'
            '<aside class="shop-cart-summary"><h2 data-shop-en="Final demo summary" data-shop-ar="الملخص التجريبي النهائي">Final demo summary</h2><div data-checkout-lines></div>'
            '<div class="shop-summary-row"><span data-shop-en="Items incl. VAT" data-shop-ar="المنتجات شاملة الضريبة">Items incl. VAT</span><strong data-checkout-items>AED 0</strong></div>'
            '<div class="shop-summary-row"><span data-shop-en="Included demo VAT (5%)" data-shop-ar="الضريبة التجريبية المشمولة (٥٪)">Included demo VAT (5%)</span><strong data-cart-vat>AED 0</strong></div>'
            '<div class="shop-summary-row"><span data-shop-en="Estimated shipping" data-shop-ar="الشحن المقدر">Estimated shipping</span><strong data-cart-shipping>AED 0</strong></div>'
            '<div class="shop-summary-row shop-summary-total"><span data-shop-en="Estimated total" data-shop-ar="المجموع المقدر">Estimated total</span><strong data-cart-total>AED 0</strong></div>'
            '<p data-shop-en="Destination duties and extra taxes are not included. These amounts are not a real offer or charge." data-shop-ar="الرسوم الجمركية والضرائب الإضافية في الوجهة غير مشمولة. هذه المبالغ ليست عرضاً أو تحصيلاً فعلياً.">Destination duties and extra taxes are not included. These amounts are not a real offer or charge.</p></aside></div></section>')
    (DIST / 'checkout.html').write_text(page(main, title=title, description=desc, active=False))


def build_order() -> None:
    title = {"en": "Demo Order Status | Destiny Furniture Shop", "ar": "حالة الطلب التجريبي | متجر ديستني"}
    desc = {"en": "Review a demo order reference and status saved on this device.", "ar": "راجع رقم الطلب التجريبي وحالته المحفوظين على هذا الجهاز."}
    main = ('<section class="shop-cart-page catalog-shell shop-order-page" data-order-page><p class="collections-kicker" data-shop-en="Order preview" data-shop-ar="معاينة الطلب">Order preview</p>'
            '<h1 data-shop-en="Your demo order" data-shop-ar="طلبك التجريبي">Your demo order</h1>'
            '<p class="shop-demo-note" data-shop-en="This reference exists only in your browser. No actual order was sent, no payment was taken, and no confirmation or status email was sent." data-shop-ar="هذا الرقم محفوظ في متصفحك فقط. لم يُرسل طلب فعلي ولم يُحصّل مبلغ ولم يُرسل بريد إلكتروني للتأكيد أو تحديث الحالة.">This reference exists only in your browser. No actual order was sent, no payment was taken, and no confirmation or status email was sent.</p>'
            '<div class="shop-order-card" data-order-details></div><a class="shop-cart-send shop-order-back" href="./products.html" data-shop-en="Continue browsing" data-shop-ar="متابعة التصفح">Continue browsing</a></section>')
    (DIST / 'order.html').write_text(page(main, title=title, description=desc, active=False))


def build_shop_data() -> None:
    items = [{key:p[key] for key in ('id','slug','category','name','image','price_aed_incl_vat','demo_stock','demo_options') if key in p} for p in PRODUCTS]
    (DIST / 'shop-data.js').write_text('window.DESTINY_PRODUCTS = ' + json.dumps(items,ensure_ascii=False,separators=(',',':')) + ';\n')
    (DIST / 'shipping-data.js').write_text('window.DESTINY_SHIPPING = ' + json.dumps(SHIPPING,ensure_ascii=False,separators=(',',':')) + ';\n')


if __name__ == "__main__":
    build_overview()
    for item in DATA["categories"]:
        build_category(item)
    for item in PRODUCTS:
        build_product(item)
    build_cart()
    build_checkout()
    build_order()
    build_shop_data()
