import logging
import scrapy
from datetime import datetime
from unicodedata import normalize
from urllib.parse import urljoin


logger = logging.getLogger(__name__)


class TripAdvisorSpider(scrapy.Spider):
  name = "trip_advisor"
  base_url = "tripadvisor.com.sg"
  allowed_domains = [base_url]
  page = 0

  def get_url(self):
    """
    Gets the starting URL to query the register's list of security blog articles.
    :return: URL that the spider starts from.
    """
    url = f"{self.base_url}/Hotels-g191-oa{self.page * 30}-United_States-Hotels.html"
    self.page += 1
    return url

  def start_requests(self):
    logger.info("Start Trip Advisor spider...")
    url = self.get_url()
    logger.info(f"Crawling {url}")
    yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    hotel_selectors_list = response.css("div.NXAUb._T")
    for hotel_selectors in hotel_selectors_list:
      path = hotel_selectors.css("div.yJIls.z.y.M0 header a::attr(href)").get()
      url = urljoin(self.base_url, path)
      name = hotel_selectors.css("div.yJIls.z.y.M0 header h3").get()
      description = hotel_selectors.css("div.OJLiL.y.M0._T span.GQeyV.d::text").get()
      hotel_data = {"url": url,
                    "name": name,
                    "description": description,
                    }
      yield hotel_data
    next_url = self.get_url()
    logger.info(f"Crawling {next_url}")
    yield scrapy.Request(url=next_url, callback=self.parse)





    # raw_links = response.xpath("//article/a[@class='story_link']/@href").getall()
    # if not raw_links:
    #   return
    # links = [urljoin(self.base_url, link) for link in raw_links]
    # # Crawl the blog article URLs found
    # yield from response.follow_all(links, self.parse_article)
    # # Continue finding more article URLs
    # next_url = self.get_url()
    # logger.info(f"Crawling {next_url}")
    # yield scrapy.Request(url=next_url, callback=self.parse)

  def parse_article(self, response):
    url = response.url
    logger.info(f"Crawling article: {url}")
    title = response.css("title::text").get().strip()
    author = response.css("div.byline_wrap a.byline::text").get().strip()
    raw_dt = " ".join(normalize("NFKD",response.xpath("string(//span[@class='dateline'])").get()).split())
    dt = datetime.strptime(raw_dt, "%a %d %b %Y // %H:%M %Z")
    contents = response.xpath("string(//div[@id='article']/div[@id='body'])").get().strip()
    article_data = {"url": url,
                    "title": title,
                    "author": author,
                    "datetime": dt,
                    "contents": contents,
                    }
    for key, value in article_data.items():
      if not value:
        logger.warning(f"Attribute data {key} is empty: '{value}'")
    yield article_data
