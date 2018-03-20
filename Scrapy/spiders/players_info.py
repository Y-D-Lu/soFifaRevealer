# -*- coding: utf-8 -*-
import scrapy
import csv


class sofifa(scrapy.Spider):
    name = "fifa"
    # prevent from redirecting
    handle_httpstatus_list = [301, 302]
    allowed_domains = ["sofifa.com"]

    # get version info from multi-task
    def __init__(self, ver=None, *args, **kwargs):
        print("Now crawling version " + ver)
        global current_ver
        current_ver = ver

    def start_requests(self):
        # get player ids from local txt file
        path = current_ver + ".txt"
        f = open(path)  # read
        lines = f.readlines()

        # start task
        for next_player in lines:
            url = next_player
            yield scrapy.Request(url=url, callback=self.parse)
        f.close()

    def parse(self, response):

        sel = scrapy.Selector(response)

        # play info

        ID = sel.xpath('//article/div[1]/div[1]/h1/text()').extract()[0].split('(ID: ')[1].split(')')[0]

        Name = sel.xpath('//html/body/section/section[1]/article/div[1]/div[1]/div/span/text()[1]').extract()[0]

        p_info = sel.xpath('//article/div[1]/div[1]/div/span/text()').extract()[-1].split(' ')

        Weight = p_info[-1].split('kg')[0]

        Height = p_info[-2].split('cm')[0]

        year = p_info[-3].split(')')[0]

        month = p_info[-5].split('(')[1]

        date = p_info[-4].split(',')[0]

        Age = p_info[-6]

        # while get a free player, set club to "Free"

        Club = sel.xpath('//article/div[1]/div[3]//td[3]//li[1]/a/text()')
        if Club:
            Club = Club.extract()[0]
            # jersey_number = sel.xpath('//article/div[1]/div[3]//td[3]//li[4]/text()').extract()[1].split('\n')[1]
        else:
            Club = 'Free'

        Nation = sel.xpath('//article/div[1]/div[1]/div/span/a/@title').extract()[0]

        Preferred_Foot = sel.xpath('//article/div[1]/div[3]//td[1]/ul/li[1]/text()').extract()[1].split('\n')[1]

        IR = sel.xpath('//article/div[1]/div[3]//td[1]/ul/li[2]/text()').extract()[1].split('\n')[1].split(' ')[0]

        Weak_Foot = sel.xpath('//article/div[1]/div[3]//td[1]/ul/li[3]/text()').extract()[1].split('\n')[1].split(
            ' ')[0]

        Skill_Moves =sel.xpath('//article/div[1]/div[3]//td[1]/ul/li[4]/text()').extract()[1].split(
            '\n')[1].split(' ')[0]

        Overall_Rating = sel.xpath('//article/div[1]/div[2]//td[1]/span/text()').extract()[0]

        Potential = sel.xpath('//article/div[1]/div[2]//td[2]/span/text()').extract()[0]

        Value = sel.xpath('//article/div[1]/div[2]//td/span/text()').extract()[2].split('€')[1].replace(
            'K','000').replace('.5M', '500000').replace('M', '000000')

        Wage = sel.xpath('//article/div[1]/div[2]//td/span/text()').extract()[3].split('€')[1].replace('K', '000')

        Crossing, Finishing, Heading_Accuracy, Short_Passing, Volleys = sel.xpath(
            '//article/div[2]/div[1]/div/ul/li/span/text()').extract()

        Dribbling, Curve, FK_Accuracy, Long_Passing, Ball_Control = sel.xpath(
            '//article/div[2]/div[2]/div/ul/li/span/text()').extract()

        Acceleration, Sprint_Speed, Agility, Reactions, Balance = sel.xpath(
            '//article/div[2]/div[3]/div/ul/li/span/text()').extract()

        Shot_Power, Jumping, Stamina, Strength, Long_Shots = sel.xpath(
            '//article/div[2]/div[4]/div/ul/li/span/text()').extract()

        Aggression, Interceptions, Positioning, Vision, Penalties = sel.xpath(
            '//article/div[3]/div[1]/div/ul/li/span/text()').extract()[0:5]

        # #before version17, there is not 'Composure' attribute
        # Composure = sel.xpath('//article/div[3]/div[1]/div/ul/li/span/text()').extract()[5]

        Marking, Standing_Tackle, Sliding_Tackle = sel.xpath(
            '//article/div[3]/div[2]/div/ul/li/span/text()').extract()

        GK_Diving, GK_Handling, GK_Kicking, GK_Positioning, GK_Reflexes = sel.xpath(
            '//article/div[3]/div[3]/div/ul/li/span/text()').extract()

        # write to csv
        csvpath = current_ver + ".csv"
        filename = (csvpath)
        csvfile = open(filename, 'a+', encoding='utf-8', newline='')
        writer = csv.writer(csvfile)
        data = [(
            ID, current_ver, Name, Weight, Height, year, month, date, Age,
            Club, Nation, Preferred_Foot, Weak_Foot, IR, Skill_Moves, Overall_Rating, Potential, Value, Wage,
            Crossing, Finishing, Heading_Accuracy, Short_Passing, Volleys,
            Dribbling, Curve, FK_Accuracy, Long_Passing, Ball_Control,
            Acceleration, Sprint_Speed, Agility, Reactions, Balance,
            Shot_Power, Jumping, Stamina, Strength, Long_Shots,
            Aggression, Interceptions, Positioning, Vision, Penalties,
            # #before version17, there is not 'Composure' attribute
            # Composure,
            Marking, Standing_Tackle, Sliding_Tackle,
            GK_Diving, GK_Handling, GK_Kicking, GK_Positioning, GK_Reflexes)
        ]

        writer.writerows(data)
        csvfile.close()
