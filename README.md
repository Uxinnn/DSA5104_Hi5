# Accommodations Database

This repository contains code used for scraping data as part of DSA5104's project. 
The project aims to build a database of accommodations for people to easily query and understand their accommodation options when travelling abroad. 
We have 2 main sources of data: AirBnB and Trip Advisor. The scrapers in this repository are built to scrape additional information from these 2 sources.

## Prerequisites

* Python3
* (Scrapy)[https://scrapy.org/]


## Trip Advisor

The trip advisor scrapers are coded using Scrapy and scrapes data from links found in CMU's Hotel Reviews dataset. 
For each hotel link, the scraper will scrape the url of the hotel's trip advisor page, the location of the hotel, and the attractions near the hotel.
The scraped data will then be combined with the data from CMU's Hotel Reviews dataset and stored in a database.


### Running the scraper

* Download the seed data from [CMU's Hotel Reviews dataset](https://www.cs.cmu.edu/~jiweil/html/hotel-review.html).
* Create the directory `/data/cmu/` and store the seed data (`offering.txt` and `review.txt`) there. 
* `cd Scrapers/trip_advisor/scrapers/scrapers`.
* `scrapy crawl trip_advisor -O trip_advisor_scraped.json`
* Scraper should start to run, data will be stored in the file `Scrapers/trip_advisor/scrapers/scrapers/trip_advisor_scraped.json`

