import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'Collections'
    allowed_domains = ['ak-plitka.ru']
    start_urls = [#'https://ak-plitka.ru/italija/',
                  #'https://ak-plitka.ru/ispanija',
                  #'https://ak-plitka.ru/kitaj/',
                  'https://ak-plitka.ru/portugalija/',
                  #'https://ak-plitka.ru/roscija/',
                  #'https://ak-plitka.ru/turcija/',
                  #'https://ak-plitka.ru/anglija/',
                  #'https://ak-plitka.ru/polsha/',
                  #'https://ak-plitka.ru/indiya/',
                  #'https://ak-plitka.ru/germanija/',
                  ]

    rules = (
             Rule(LinkExtractor(allow=('/portugalija/'), deny=()), follow=True, callback='parse',),)

    def parse(self, response):        
        for collection in response.css('div.product-small-item'):
            link_to_collection = f'https://ak-plitka.ru{collection.css("a.product-small-item__overlay-link::attr(href)").get()}'
            yield scrapy.Request(link_to_collection, callback=self.parse_collection,
                                 meta = {'Term Permalink' : link_to_collection,
                                         'Term Name' : collection.css('span::text').get(),
                                         'Count': collection.css('div.product-small-item__icon-specs > div > span::text').get(),
                                         'Attribute Value (pa_country)': collection.css('span.country::text').get(),
                                         })
            
    def parse_linkcollection(self, response):
        for collection in response.css('div.product-small-item'):
            link_to_collection = collection.css('a.product-small-item__overlay-link::attr(href)').get()
            yield response.follow(link_to_collection, callback=self.parse_collection)
           
    def parse_collection(self, response):
        meta_description = response.xpath('//meta[@name="description"]//@content').get()
        keywords = response.xpath('//meta[@name="keywords"]//@content').get(),
        description = ''.join(response.xpath('//div[@class="ap-su-info__section-text mask"]/node()').getall()).strip().replace("<span>", "").replace("</span>", "").replace("\r\n", "").replace("\t", "")
        title = response.css('title::text').get()
        parent_name = ''.join(response.xpath('//ul[@class="ap-su-info__list"]/li/a/text()').get())
        image = '|'.join(response.css('div.carousel-item>div::attr(style)').getall())
        pdf = response.xpath('//ul[@class="ap-su-info__list"]/li[9]/a/@href').get()
        pa_factory = response.xpath('//ul[@class="ap-su-info__list"]/li/span/text()').get()
        pa_country = response.xpath('//ul[@class="ap-su-info__list"]/li[2]/span/text()').get()
        pa_priceLevel = response.xpath('//ul[@class="ap-su-info__list"]/li[7]/span/text()').get()
        priceLevel = response.xpath('//ul[@class="ap-su-info__list"]/li[7]/text()').get()
        pa_paymentType = response.xpath('//ul[@class="ap-su-info__list"]/li[8]/span/text()').get()
        paymentType = response.xpath('//ul[@class="ap-su-info__list"]/li[8]/text()').get()
        pa_inShowRoom = response.xpath('//ul[@class="ap-su-info__list"]/li[4]/span/text()').get()
        inShowRoom = response.xpath('//ul[@class="ap-su-info__list"]/li[4]/text()').get()
        pa_deliveryType = response.xpath('//ul[@class="ap-su-info__list"]/li[3]/span/text()').get()
        deliveryType = response.xpath('//ul[@class="ap-su-info__list"]/li[3]/text()').get()
        pa_categories = response.xpath('//ul[@class="ap-su-info__list"]/li[5]/span/text()').get()
        categories = response.xpath('//ul[@class="ap-su-info__list"]/li[5]/text()').get()
        pa_tileType = response.xpath('//ul[@class="ap-su-info__list"]/li[6]/span/text()').get()
        tileType = response.xpath('//ul[@class="ap-su-info__list"]/li[6]/text()').get()
        name = response.xpath('//span[@class="ap-breadcrumbs__link"]//text()').get()
        result = {'Term Permalink': response.meta['Term Permalink'],    
             'Term Name': response.meta['Term Name'],
             'Term Name Path': f'{response.meta["Attribute Value (pa_country)"]}->{parent_name}->{name}',
             'Term Parent Name': parent_name,
             'Description' : description,
             'Title' : title,
             'MetaDescription': meta_description,
             'MetaKeywords': ''.join(keywords),
             'Count': response.meta['Count'],
             'Url Image': image.replace("background-image: url('","https://ak-plitka.ru").replace("?width=1200&height=500')",""),
             'PDF': pdf,
             'Attribute Name (pa_factory)' : pa_factory,
             'Attribute Value (pa_factory)' : ''.join(parent_name),
             'Attribute Name (pa_country)' : pa_country,
             'Attribute Value (pa_country)': response.meta['Attribute Value (pa_country)'],
             'Attribute Name (pa_priceLevel)' : pa_priceLevel,
             'Attribute Value (pa_priceLevel)' : priceLevel,
             'Attribute Name (pa_paymentType)' : pa_paymentType,
             'Attribute Value (pa_paymentType)' : paymentType,
             'Attribute Name (pa_inShowRoom)' : pa_inShowRoom,
             'Attribute Value (pa_inShowRoom)' : inShowRoom,
             'Attribute Name (pa_deliveryType)' : pa_deliveryType,
             'Attribute Value (pa_deliveryType)' : deliveryType,
             'Attribute Name (pa_categories)' : pa_categories,
             'Attribute Value (pa_categories)' : categories,
             'Attribute Name (pa_tileType)' : pa_tileType,
             'Attribute Value (pa_tileType)' : tileType, 
             }
        return result


  
