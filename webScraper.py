from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd



class ReviewScraper:
    def __init__(self, url):
        self.url = url
        self.file = None
        self.writer = None
    
    

    def open_file(self):
        self.file = open("Letterboxd_scraped_reviews.csv", "w", encoding="utf-8", newline='')
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow(["ID", "Reviews"])

    def close_file(self):
        if self.file:
            self.file.close()

    def scrape_reviews(self, desired_comments):
        id_list = [] 
        review_list = []
        desired_comments = 500
        self.open_file()
        page_number = 1
        comments_count = 0

        while comments_count < desired_comments:
            url_with_page = f"{self.url}/page/{page_number}"
            page_to_scrape = requests.get(url_with_page)
            soup = BeautifulSoup(page_to_scrape.text, "html.parser")
            reviews = soup.findAll("div", attrs={"class": "body-text -prose collapsible-text"})

            for review in reviews:
                print(review.text)
                id_list.append(comments_count + 1)
                review_list.append(review.text.strip())  # Write each review as a separate row
                
                comments_count += 1
                

                if comments_count >= desired_comments:
                    break

            next_link = soup.find("a", class_="next")

            if next_link:
                page_number += 1
            else:
                break
        
        
        self.writer.writerows(zip(id_list, review_list))
        self.close_file()


if __name__ == "__main__":
    scraper = ReviewScraper("https://letterboxd.com/film/about-time/reviews/")
    scraper.scrape_reviews(500)
   # df = pd.read_csv('Letterboxd_scraped_reviews.csv')
    #print(df.shape[0])
    