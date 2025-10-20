import scrapy

class MatchItem(scrapy.Item):
    match_id = scrapy.Field()
    date = scrapy.Field()
    home = scrapy.Field()
    away = scrapy.Field()
    score = scrapy.Field()
    league = scrapy.Field()
    season = scrapy.Field()
