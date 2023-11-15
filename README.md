# Accommodations Database

This repository contains code used for scraping data as part of DSA5104's project. 
The project aims to build a database of accommodations for people to easily query and understand their accommodation options when travelling abroad. 
We have 2 main sources of data: AirBnB and Trip Advisor. The scrapers in this repository are built to scrape additional information from these 2 sources.

## Prerequisites

* Python3
* [Scrapy](https://scrapy.org/)
* [Selenium](https://selenium-python.readthedocs.io/)
* [Chromedriver](https://googlechromelabs.github.io/chrome-for-testing/)

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


### Data Processing

The scraped data are then combined with the raw data from the source datasets into formats that can be uploaded to MySQL and MongoDB. 
Notebooks used for the processing of the data can be found under the `data_processing` directory.

## AirBnB

The AirBnB scrapers are based on Selenium and scrapes user location data from reviewer_id column found in AirBnB's `reviews.csv` data file, and attractions for each city from TripAdvisor website. 
For each reviewer_id, `scrapper.py` will scrape the location of the reviewer via the url `https://www.airbnb.com.sg/users/show/:id`
For each city, `scrapper_attraction.py` will scrape attractions found in the city.
The scraped data will then be combined with the data from AirBnB's dataset and stored in a database.


### Running the scraper

* Download the data from [AirBnB's dataset](http://insideairbnb.com/get-the-data/).
* Extract `reviews.csv` for a city of choice into `Scrapers/airbnb`
* Run `scrapper.py`
* Data would be generated as `user_loc.csv` in the same folder
* Replace `search_query` variable value in `scrapper_attraction.py`
* Run `scrapper_attraction.py`
* Data would be generated as `attractions.csv` in the same folder

### Data Processing

Scraped user location data is combined with the raw data by running `joiner.py`. Due to decreased network connection speed with AirBnB, possibly due to detection of scrapping activities, only a small subset of user location was scrapped as a POC, and the rest were randomly generate from the scrapped data.

The scraped data are then combined with the raw data from the source datasets and directly manipulated into the correct document schemas, and uploaded into MongoDB. This is done using `mongo.py`