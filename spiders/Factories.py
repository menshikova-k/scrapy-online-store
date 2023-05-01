import scrapy

class FactoriesSpider(scrapy.Spider):
    name = 'Factories'
    allowed_domains = ['ak-plitka.ru']
    start_urls = [#'https://ak-plitka.ru/italija/',
                  #'https://ak-plitka.ru/ispanija',
                  #'https://ak-plitka.ru/kitaj',
                  #'https://ak-plitka.ru/portugalija',
                  #'https://ak-plitka.ru/roscija',
                  #'https://ak-plitka.ru/turcija',
                  #'https://ak-plitka.ru/anglija',
                  #'https://ak-plitka.ru/polsha',
                  'https://ak-plitka.ru/indiya',
                  #'https://ak-plitka.ru/germanija/',
                  ]

            
    def parse(self, response):
        for factory in response.css('div.ap-countries__item'):
            link_to_factory = f'https://ak-plitka.ru{factory.css("a.ap-countries__overlay-link::attr(href)").get()}'
            img = factory.css('div.ap-countries__flag::attr(style)')
            yield scrapy.Request(link_to_factory, callback=self.parse_factories,
                                 meta = {'Term Permalink': link_to_factory,
                                         'Term Name':factory.css('h4.ap-countries__country::text').get(),
                                         'Count':factory.css('strong::text').get(),
                                         'Image URL': img.get().replace("background-image: url('","https://ak-plitka.ru").replace("?width=218&height=146')",""),
                                         })
            
    def parse_linkfactory(self, response):
        for factory in response.css('div.ap-countries__item'):
            link_to_factory = factory.css('a.ap-countries__overlay-link::attr(href)').get()
            yield response.follow(link_to_factory, callback=self.link_to_factory)

    def parse_factories(self, response):
        description = ''.join(response.xpath('//div[@class="ap-cat-brand__text mask"]/node()').getall()).strip().replace("<span>", "").replace("</span>", "").replace("\r\n", "").replace("<div>", "").replace("</div>", "").replace("\t", "")
        title = response.css('title::text').get()
        metadescription = response.xpath('//meta[@name="description"]//@content').get()
        keywords = response.xpath('//meta[@name="keywords"]//@content').get()
        country = response.css('small.ap-cat-brand__meta>span::text').get()
        result = {'Term Permalink': response.meta['Term Permalink'],
             'Term Name': response.meta['Term Name'],
             'Term Name Path': f'{country}->{response.meta["Term Name"]}',
             'Term Parent Name': country,
             'Description' : description,
             'MetaTitle': ''.join(title),
             'MetaDescription' : ''.join(metadescription),
             'MetaKeywords' : ''.join(keywords),
             'Count': response.meta['Count'],
             'Image URL': response.meta['Image URL'].replace("?width=233&height=156')",""),
            }
        
        return result



        
