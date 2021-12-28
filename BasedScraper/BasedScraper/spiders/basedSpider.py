import scrapy

class  BasedSpider(scrapy.Spider):
    name = 'based'
    start_urls = ['https://biblija.ks.hr']

    def parse(self, response):

        urls = response.css('li.bible-books-item a::attr(href)').getall()
        books = response.css('li.bible-books-item a::text').getall()
        for i, url in enumerate(urls):
            url = urljoin(response.url, url)
            yield {
                'knjiga': books[i],
                'poglavlja': scrapy.Request(url=url, callback=self.parse_poglavlja)
            }

    def parse_poglavlja(self, response):
        yield{
            'broj_poglavlja': response.css('span.chapter-number ::text').get(),
            'glave': response.css('span.bible-line ::text').getall()                
        }
        next_page = response.css('a.chapter-next ::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse )