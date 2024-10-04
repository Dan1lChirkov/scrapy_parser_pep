import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        section = response.css('section[id="numerical-index"]')
        num_table_link = section.css('a.reference.internal::attr(href)').get()
        yield response.follow(num_table_link, callback=self.parse_num_pep)

    def parse_num_pep(self, response):
        all_peps = response.xpath(
            '//a[@class="pep reference internal"]/@href').getall()
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        full_pep_name = response.css('.page-title::text').get().split()
        number = full_pep_name[1]
        name_pep = ' '.join(full_pep_name[3:])
        data = {
            'number': int(number),
            'name': name_pep,
            'status': response.css('abbr::text').get()
        }
        yield PepParseItem(data)
