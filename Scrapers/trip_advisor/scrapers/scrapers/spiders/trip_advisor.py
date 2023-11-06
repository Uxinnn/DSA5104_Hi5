import logging
import scrapy
import json


logger = logging.getLogger(__name__)


class TripAdvisorSpider(scrapy.Spider):
  name = "trip_advisor"
  base_url = "tripadvisor.com.sg"
  allowed_domains = [base_url]
  data_path = "../../../../data/cmu/offering.txt"

  def start_requests(self):
    logger.info("Start Trip Advisor spider...")
    with open(self.data_path, 'r') as f:
      for hotel_data in f:
        hotel_data = json.loads(hotel_data.strip())
        url = hotel_data["url"]
        logger.info(f"Crawling {url}")
        yield scrapy.Request(url=url,
                             callback=self.parse
                             )

  def parse(self, response):
    """
    Have to creative with selectors since webpage uses dynamic css class names.
    """
    url = response.url
    if "Hotel_Review" not in url:
      return
    logger.info(f"Crawling article: {url}")
    # Use 'Write a review' as anchor to find location
    location = response.xpath("//div[contains(text(), 'Write a review')]/../../..//preceding-sibling::div/span/span/text()").get().strip()
    city = location.split(",")[1].strip()
    # Use nav tag as anchor
    country = response.css("li.breadcrumb span::text")[0].get().strip()
    # country = response.xpath("//nav/following-sibling::div/div/div/div/a/span/span/text()")[0].get()
    # Use 'Getting there' as anchor to find attractions
    attractions = response.xpath("//div[contains(text(), 'Getting there')]/../../../../following-sibling::div/div/div/div/a/div/div/text()").getall()
    attractions = [attraction for attraction in attractions if len(attraction) > 2]
    article_data = {"url": url,
                    "location": location,
                    "city": city,
                    "country": country,
                    "attractions": attractions
                    }
    for key, value in article_data.items():
      if not value:
        logger.warning(f"Attribute data {key} is empty: '{value}'")
    yield article_data
