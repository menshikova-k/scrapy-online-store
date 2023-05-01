import scrapy

        
class CountriesSpider(scrapy.Spider):
    name = 'Countries'
    allowed_domains = ['ak-plitka.ru']
    start_urls = ['https://ak-plitka.ru/countries/']

    def parse(self, response):
        for country in response.css('div.ap-countries__item'):
            link_to_country = f'https://ak-plitka.ru{country.css("a.ap-countries__overlay-link::attr(href)").get()}'
            yield scrapy.Request(link_to_country, callback=self.parse_countries,
                                   meta = {'link_to_country': link_to_country,
                                           'name': country.css('h4.ap-countries__country::text').get(),
                                           'image': country.css('div.ap-countries__flag::attr(style)').get().replace("url('","https://ak-plitka.ru").replace("?width=218&height=146')",""),
                                           'count': country.css('strong::text').get(),
                                           })

    def parse_linkcountries(self, response):
        for i in response.css('div.ap-static-page__content'):
            link_to_country = i.css('a.ap-countries__overlay-link::attr(href)').get()
            yield response.follow(link_to_country, callback=self.parse_countries)

    def parse_countries(self, response):
        description = response.xpath('//article[@class="mask"]/node()').get()
        metatitile = response.css('title::text').get()
        metadescription = response.xpath('//meta[@name="description"]//@content').get()
        metakeywords = response.xpath('//meta[@name="keywords"]//@content').get()

        result = {'Term Permalink': response.meta['link_to_country'],
             'Term Name Path': response.meta['name'],
             'Term Name': response.meta['name'],
             'Description': description,
             'MetaTitile': metatitile,
             'MetaDescription': metadescription,
             'MetaKeywords': metakeywords,
             'Count': response.meta['count'],
             'Image URL': response.meta['image'],
             }
        return result
        
