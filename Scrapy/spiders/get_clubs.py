import csv
import scrapy


class getPlayers(scrapy.Spider):
    name = "club"
    # prevent from redirecting so as to crawl a little more to get all players
    handle_httpstatus_list = [301, 302]

    def start_requests(self):
        path = "ver_list.txt"
        f = open(path)  # read from version list

        lines = f.readlines()
        for ver in lines:
            for i in range(0, 720, 80):
                url = 'https://sofifa.com/teams/club?' + ver + '&set=true&offset=' + str(i)
                yield scrapy.Request(url=url, callback=self.parse)
        f.close()

    def parse(self, response):
        if response.body != b'':
            sel = scrapy.Selector(response)
            # get players' links
            club_name = sel.xpath(
                '//*[@id="pjax-container"]/table/tbody/tr/td[2]/div/a/text()').extract()
            club_id = sel.xpath(
                '//*[@id="pjax-container"]/table/tbody/tr/td[2]/div/a/@href').extract()
            club_league = sel.xpath(
                '//*[@id="pjax-container"]/table/tbody/tr/td[2]/div/div/a/text()').extract()
            club_nation = sel.xpath(
                '//*[@id="pjax-container"]/table/tbody/tr/td[3]/div/a/text()').extract()
            if (club_name):
                csvfile = open(response.url.split('?')[1].split('%')[0] + ".csv", 'a+', encoding='utf-8', newline='')
                writer = csv.writer(csvfile)
                for i in range(club_name.__len__()):
                    data = [(club_name[i], club_id[i].split('/team/')[1], club_league[i], club_nation[i])]
                    writer.writerows(data)
                csvfile.close()
