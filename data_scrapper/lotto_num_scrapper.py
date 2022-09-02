from scrapy import Selector
from scrapy.crawler import CrawlerProcess
import requests
import pandas as pd

html = ""

url = "https://www.loteriasyapuestas.es/es/resultados/euromillones"

html = requests.get(url).content

# Number locations
basic_numbers_loc = 'combinacion-li--euromillones'
star_numbers_loc = 'estrellas-li'

sel = Selector(text = html)

basic_numbers = sel.xpath(f'//li[contains(@class,"{basic_numbers_loc}")]//text()').extract()
star_numbers = sel.xpath(f'//li[contains(@class,"{basic_numbers_loc}")]//text()').extract()

print(basic_numbers + star_numbers)

#Save to html
# with open('page.html', 'w') as f:
#     f.write(html.decode("utf-8"))