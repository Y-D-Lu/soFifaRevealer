import scrapy


class getPlayers(scrapy.Spider):
    name = "check"
    # prevent from redirecting so as to crawl a little more to get all players
    handle_httpstatus_list = [301, 302]

    def __init__(self, ver=None, *args, **kwargs):
        # define a global var for request
        global vers
        vers = ver

    def start_requests(self):
        # get to upon 20000 players to insure that all the players are here
        for i in range(0, 20000, 80):
            url = 'https://sofifa.com/players?' + vers + '&set=true&offset=' + str(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.body != b'':
            sel = scrapy.Selector(response)
            # get players' links
            urls = sel.xpath(
                '// *[ @ id = "pjax-container"] / table / tbody / tr/ td[2] / div / a[2] / @href').extract()
            txtname = vers + ".txt"
            for url in urls:
                d = open(txtname, "a+", encoding='utf-8', newline='')
                # add more features to make it easier for next step
                d.write('https://sofifa.com' + url + '?' + vers + "&set=true&units=mks&currency=EUR&hl=en-US" + "\r\n")
            d.close()
