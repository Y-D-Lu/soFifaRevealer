import scrapy


class GetVersions(scrapy.Spider):
    name = "version"
    # prevent from redirecting
    handle_httpstatus_list = [301, 302]

    def start_requests(self):
        # crawl data from sofifa.com
        url = 'https://sofifa.com'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # be sure the body of the response is not empty
        if response.body != b'':
            sel = scrapy.Selector(response)
            # get version list
            versions = (sel.xpath('//*[@id="version-calendar"]/div/div/div[2]/div/div/div[2]/ a / @href').extract())
        for ver in versions:
            # clip for further use
            ver = ver.split('/?')[1].split('&set')[0]
            # save to local as txt file
            d = open("ver_list.txt", "a+", encoding='utf-8', newline='')
            d.write(ver + "\r\n")
        d.close()
