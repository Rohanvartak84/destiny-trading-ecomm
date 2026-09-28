# Destiny Furniture Shop Demo

A **separate** English/Arabic ecommerce preview based on the existing Destiny General Trading LLC design. The original enquiry website is unchanged.

## Preview features

- Sixteen provisional products in four categories. Twelve standard products have demo AED prices, sample stock levels, filters, sorting and size/finish choices. Four custom products use a product-prefilled enquiry form rather than a cart.
- Product records have an `images` array and a thumbnail gallery when more than one image exists. The current project has **one illustrative image per product**; genuine client photos are needed before launch.
- The device-local cart saves selected options and quantities, enforces sample stock limits, and allows removal.
- `catalog/shipping.json` contains **illustrative** flat rates for ten countries, with standard and express methods. Other countries require a shipping quotation. The cart and guest checkout both show item prices including illustrative UAE VAT, the included VAT portion, estimated shipping, and the total **including shipping**. Shipping is not added twice. Destination duties or additional taxes are not modelled.
- Guest checkout collects contact and delivery details locally for the active form. It lets the shopper select a demo payment method without collecting card data. Submitting creates a **local demo order preview** with a reference and status page. It neither sends the address to a server nor places an actual order.

**There is no live payment, order backend, transactional email or remote tracking.** The order confirmation explicitly says no email was sent. Do not use this preview to accept real orders or make actual tax/shipping promises.

## What is needed for a live store

1. Confirmed product catalogue, multiple real photos per product, stock source, variant prices and fulfilment rules.
2. Business-approved shipping rates or a carrier integration for all supported destinations, and verified tax/duty rules.
3. Payment processor account and backend checkout/session integration.
4. Durable order database, transactional email provider with verified sending domain, and a process to update fulfilment status and send customer notifications.
5. Privacy, returns, shipping and terms policies approved by the client.

## Deploy on Vercel

The static preview is in `dist/`. `vercel.json` publishes this directory; no build command or environment variables are needed. Extract the archive, run `npx vercel login`, then `npx vercel` for a preview and `npx vercel --prod` to publish. Or import this folder from Git into Vercel using **Other** framework and `dist` output directory.

Edit `catalog/products.json` and `catalog/shipping.json`, then run `python3 scripts/build_catalog.py` to regenerate the catalogue, cart, checkout, order page and browser data files. The cart and demo order references live only in that browser's local storage. Verify the WhatsApp number and placeholder email before any public launch.
