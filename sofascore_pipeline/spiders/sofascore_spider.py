import scrapy
from sofascore_pipeline.items import MatchItem

class SofascoreSpider(scrapy.Spider):
    name = "sofascore"
    custom_settings = {
        "FEEDS": {
            "data/raw/matches.csv": {"format": "csv", "overwrite": True}
        }
    }

    def __init__(self, league=None, season=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.league = league
        self.season = season

    def start_requests(self):
        # Ponto de partida (exemplo ilustrativo)
        url = "https://www.sofascore.com/"
        yield scrapy.Request(url, callback=self.parse_home)

    def parse_home(self, response):
        # TODO: implementar lógica de descoberta de ligas/partidas
        # Exemplo: apenas gera um item fictício de demonstração
        item = MatchItem(
            match_id="demo-0001",
            date="2025-01-01",
            home="Home FC",
            away="Away FC",
            score="2-1",
            league=self.league or "DEMO",
            season=self.season or "2025",
        )
        yield item