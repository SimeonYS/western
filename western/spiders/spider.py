import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import WesternItem
from itemloaders.processors import TakeFirst
import json
pattern = r'(\xa0)?'

class WesternSpider(scrapy.Spider):
	name = 'western'
	start_urls = ['https://www.westernalliancebancorporation.com/webapi/NewsListing/NewsArticles/?filterTags=&page=%7B8A208D9F-59DD-4905-A6A1-C4EFBBDCF64C%7D&tags=%7B12889507-56A9-4DEF-B0B5-A460993D351D%7D']

	def parse(self, response):
		data = json.loads(response.text)
		for index in range(len(data)):
			link = data[index]['cta_link']
			yield response.follow(link, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//ul[@class="author__details"]/li[last()]/text()').get().strip()
		title = response.xpath('//h2/text()').get()
		content = response.xpath('//div[@class="content__body"]//text()[not (ancestor::div[@style="margin-top: 20px;"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=WesternItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
