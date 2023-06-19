from bs4 import BeautifulSoup
import requests
from PyQt6.QtCore import QThread, pyqtSignal
import csv



class ReviewScraper(QThread):
    scrapingComplete = pyqtSignal()
    scrapingProgress = pyqtSignal(int)

    def __init__(self, url, desired_comments):
        super().__init__()
        self.url = url
        self.desired_comments = desired_comments
        self.file = None
        self.writer = None
    
    

    def open_file(self):
        self.file = open("Letterboxd_scraped_reviews.csv", "w", encoding="utf-8", newline='')
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow(["ID", "Reviews"])

    def close_file(self):
        if self.file:
            self.file.close()

    def run(self):
        id_list = [] 
        review_list = []
        desired_comments = 500
        self.open_file()
        page_number = 1
        comments_count = 0

        while comments_count < desired_comments:
            if "https://" not in self.url:
                self.url = "https://"+self.url
            url_with_page = f"{self.url}/page/{page_number}"
            page_to_scrape = requests.get(url_with_page)
            soup = BeautifulSoup(page_to_scrape.text, "html.parser")
            reviews = soup.findAll("div", attrs={"class": "body-text -prose collapsible-text"})

            for review in reviews:
                print(review.text)
                id_list.append(comments_count + 1)
                review_list.append(review.text.strip())  # Write each review as a separate row
                progress = int((comments_count/desired_comments)*(100))
                self.scrapingProgress.emit(progress)
                
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
        self.scrapingComplete.emit()
    



