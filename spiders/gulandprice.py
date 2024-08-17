import scrapy

class GulandSpider(scrapy.Spider):
    name = 'gulandprice'
    allowed_domains = ['guland.vn']
    start_urls = ['https://guland.vn/mua-ban-bat-dong-san-ha-noi']
    
    # Số trang cuối cùng mà bạn muốn crawl
    max_pages = 10  # Bạn có thể thay đổi giá trị này tùy thuộc vào số lượng trang bạn muốn crawl

    def parse(self, response):
        products = response.css('div.c-sdb-card')
        for guland in products:
            item = {
                'name': guland.css('div.c-sdb-card__tle > a::text').get(),
                'price': guland.css('span.sdb-inf-data b::text').get(),
                'location': next((text.strip() for text in guland.css('span.sdb-inf-data::text').getall() if ',' in text and 'Hà Nội' in text), None),
                'floor_area': guland.css('span.sdb-inf-data.data-size-lg b::text').get(),
                'link': response.urljoin(guland.css('div.c-sdb-card__tle > a::attr(href)').get())
            }
            yield item

        # Lấy số trang hiện tại từ URL hoặc đặt là 1 nếu không tìm thấy
        current_page = response.url.split('=')[-1]
        self.log(f'Current page: {current_page}', level=scrapy.log.INFO)
        
        if current_page.isdigit():
            current_page_number = int(current_page)
        else:
            current_page_number = 1

        self.log(f'Current page number: {current_page_number}', level=scrapy.log.INFO)

        # Tính toán số trang tiếp theo
        next_page_number = current_page_number + 1

        # Tạo URL cho trang tiếp theo
        if next_page_number <= self.max_pages:
            next_page_url = f'https://guland.vn/mua-ban-bat-dong-san-ha-noi?page={next_page_number}'
            self.log(f'Next page URL: {next_page_url}', level=scrapy.log.INFO)
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.log('Reached the max number of pages to crawl.', level=scrapy.log.INFO)
