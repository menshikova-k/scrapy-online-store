import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'Products'
    allowed_domains = ['ak-plitka.ru']
    start_urls = ['https://ak-plitka.ru/italija/rex/']
    rules = (
             Rule(LinkExtractor(allow=('/rex/'), deny=()), follow=True, callback='parse',),)
    

    def parse(self, response):
        for product in response.css('div.product-small-item.product-small-item_type2'):
            link_to_product = f'https://ak-plitka.ru{product.css("p.product-small-item__title > a::attr(href)").get()}'
            yield scrapy.Request(link_to_product, callback=self.parse_product,
                                  meta = {'type_name': response.xpath('//ul[@class="ap-su-info__list"]/li[6]/span/text()').get(),
                                          'type_value': response.xpath('//ul[@class="ap-su-info__list"]/li[6]/text()').get(),
                                          'unit_name': response.xpath('//div[@class="product-small-item__specs"]/p[1]/text()').get(),
                                          'unit_value': response.xpath('//div[@class="product-small-item__specs"]/p[2]/text()').get(),                                                                                  
                                          'collection_img': response.css('div.carousel-item>div::attr(style)').get().replace("background-image: url('","https://ak-plitka.ru").replace("?width=1200&height=500')",""), 
                                          })

    def parse_product(self, response):
        product = response.css('div.ap-content__inner')
        link_to_product = product.css('p.product-small-item__title > a::attr(href)').get()
        title = response.css('h1.ap-single-unit__title::text').get()
        img_product = response.xpath("//div[@class='ap-single-unit__photo']/img/@src").get().replace("/Gallery/","https://ak-plitka.ru/Gallery/").replace('?&height=430','')    
        Collection = response.xpath('//ul/li[3]/a/text()').get()
        Factory = response.xpath('//ul/li[1]/a/text()').get()
        result = {
            'Title': title,
            'Sku': response.xpath('//ul/li[4]/text()').getall()[1].strip(),
            'Price': product.css('strong::text').get(),
            'Slug': title.lower().replace(' ','-'),    
            'Product Type': 'Simple',
            'Image URL': img_product,
            'Attribute Name (pa_type)': response.meta['type_name'],
            'Attribute Value (pa_type)': response.xpath('//ul/li[5]/text()').getall()[1].strip(),#заходим внутрь
            'Attribute Name (pa_surface)': response.xpath('//ul/li[6]/span/text()').getall()[1].strip(),
            'Attribute Value (pa_surface)': response.xpath('//ul/li[6]/text()').getall()[1].strip(),
            'Attribute Name (pa_retified)': response.xpath('//ul/li[7]/span/text()').getall()[1].strip(),
            'Attribute Value (pa_retified)': response.xpath('//ul/li[7]/text()').getall()[1].strip(),
            'Attribute Name (pa_size)': response.xpath('//div[@class="ap-single-unit__icon"][1]/span/text()').get(),
            'Attribute Value (pa_size)': response.xpath('//div[@class="ap-single-unit__icon"][1]/strong/text()').get(),
            'Attribute Name (pa_inpack)': "Штук в коробке",
            'Attribute Value (pa_inpack)': response.xpath('//div[@class="ap-single-unit__icon"][2]/strong/text()').get(),
            'Attribute Name (pa_unit)': response.meta['unit_name'],
            'Attribute Value (pa_unit)': response.meta['unit_value'],
            'Категории товара': ''.join(response.xpath('//nav[@class="ap-breadcrumbs"]//text()')[4:-1].getall()).replace('\r\n', '>'),
            'Factory': Factory,
            'Collection': f'{Factory} {Collection}', 
            'CollectionImages': response.meta['collection_img'],
            'ProductUrl': response.url, 
            }
        return result
