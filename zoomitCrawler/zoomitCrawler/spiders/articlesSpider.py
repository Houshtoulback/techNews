import scrapy
import json




class ArticlesSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        'https://api2.zoomit.ir/editorial/api/articles/browse?sort=Newest&publishPeriod=All&readingTimeRange=LessThan5Min&pageNumber=1&PageSize=200'
    ]

    def parse(self, response):
        data = json.loads(response.body)
        articles = data.get('source', [])

        for article in articles:
            article_data = {
                'title': article.get('title'),
                'author': article.get('author', {}).get('fullName'),
                'detail_url': f"https://www.zoomit.ir/{article.get('slug')}" 
            }

            yield scrapy.Request(article_data['detail_url'], callback=self.parse_article_detail, meta={'article_data': article_data})

    
        if data.get('hasNext'):
            current_page = data.get('currentPage', 1)
            total_pages = data.get('totalPages', 1)
            next_page = current_page + 1
            if next_page <= total_pages:
                next_page_url = response.url.replace(f'pageNumber={current_page}', f'pageNumber={next_page}')
                yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article_detail(self, response):
        article_data = response.meta['article_data']

        tags = response.css('div.flex__Flex-le1v16-0.oNOID a::attr(href)').getall()

        article_data['tags'] = tags

        # Scrape all text from all p tags with the specified class name
        paragraphs = response.css('p.typography__StyledDynamicTypographyComponent-t787b7-0.fZZfUi.ParagraphElement__ParagraphBase-sc-1soo3i3-0.gOVZGU::text').getall()
        article_data['content'] = ' '.join(paragraphs)


        yield article_data
