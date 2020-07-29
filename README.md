# Dianping-Web-Crawler #

## Introduction ##
Everyone knows that China is an extremely gastronomic-centric culture where much time and effort is put into finding the best restaurants. For foodies in China, many of them turn to [Dianping](http://www.dianping.com/) (full name: Dazhongdianping), a Chinese Internet company that provides services of “online consumer guide”, covering more than 500,000 restaurants in over 300 cities in China. On the website, consumers can share their experiences on food by giving reviews and rating.

There is a great amount of data on Dianping.com which can be used for later analysis, so I write this web crawler trying to extract the information about restaurants, comments and users from the website. My work is focusing on the data of restaurants in Guangzhou, China. I upload all my code files and the data I've scraped so far to this repository.

## Data So Far ##
* 750 restaurants
* 20,000+ users
* 100,000+ comments

## About My Code ##
* Programming language
  * Python 2.7
* Frameworks
  * [Scrapy](https://scrapy.org/)
  * [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* Database tool
  * [Toad Mac Edition](http://www.toadworld.com/products/toad-mac-edition/) - MongoDB GUI
* Some code files
  * *main.py* - Use the `scrapy crawl <spider>` command to run the spider
  * *item.py* - Define the data field
  * *pipelines.py* - Export the data to MongoDB
  * *spider/* - Define the spiders used to scrape data of restaurants, comments and users
