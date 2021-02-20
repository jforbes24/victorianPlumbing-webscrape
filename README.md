# victorianPlumbing-webscrape
Scrapes entire victorianplumbing.co.uk website and returns full product catalogue range and attributes, then saves down to a .xlsx file.

!Python3

Scrape environment created using Requests and BeautifulSoup, selecting randomly 1 of 6 user-agents.

Iterates through all category and product pages whilst handling pagination, stores all product links and retrieves the following attributes from each individual product detail page:

Attributes saved to dictionary:

- Sku/Model number
- Product description
- Price / Previous RRP ('Was')
- Category heirarchy
- Product rating
- Number of reviews
- Customer reviews
- Availability
- Lead time
- Number of product images

Dashboard examples surfaced via Power BI
