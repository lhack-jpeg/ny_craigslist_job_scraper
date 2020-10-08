import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/d/jobs/search/jjj']

    def parse(self, response):

        listings = response.xpath('//li[@class="result-row"]')
        for listing in listings:
        	date = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
        	link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
        	text = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()
        	# you can use the meta={} like a yield when you want to move the data points to a
        	# parse method
        	yield scrapy.Request(link, callback=self.parse_job, meta={'date':date, 'link':link, 'text':text})
        next_page_url = response.xpath('//*[@class="button next"]/@href').extract_first()
        if next_page_url:
        	yield scrapy.Request(response.urljoin(next_page_url), callback = self.parse)

    def parse_job(self, response):
    	date = response.meta['date']
    	link = response.meta['link']
    	text = response.meta['text']
    	compensation = response.xpath('//*[contains(text(), "compensation:")]/b/text()').extract()
    	employment = response.xpath('//*[contains(text(), "employment type:")]/b/text()').extract()
    	description = response.xpath('//*[@id="postingbody"]/text()').extract()
    	yield{
    		"Date" : date,
    		"link" : link,
    		"Text" : text,
    		"Employment" : employment,
    		"Compensation" : compensation,
    		"Job description" : description
    	}