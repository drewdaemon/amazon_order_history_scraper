Amazon Order History Scraper
=====
## Current functionality

- Supports both Amazon personal and business accounts
- Gathers order history information within specified date range
- Generates csv and saves invoices as html files
- Scrapes following order history information
  - Order ID
  - Date
  - Title
  - Quantity
  - Seller
  - Condition
  - Purchase Price Per Unit
  - Subtotal
  - Shipping
  - Sales Tax
  - Total for Shipment
  - Total for Order
  - Payment Method
  - Transaction Date
  - Date Shipped

## Getting Started

- Make sure you have Python and Firefox installed (the scraper is *incompatible with Firefox 47*.  You need Firefox [46](https://ftp.mozilla.org/pub/firefox/releases/46.0b9/) or [45](https://ftp.mozilla.org/pub/firefox/releases/45.2.0esr/).)
- Download/clone the repository
- Create invoices/ and csvs/ directories in downloaded folder (this is where the generated files will be stored)
- Update scrapespecs.xml to include your credentials, timespan, and account type
- Run scrape.py

## Known Issues
- Script reportedly has trouble reading xml file on windows systems
- Incompatibitity with Firefox 47 (someone needs to update the script to function with [Marionette](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette))