from bs4 import BeautifulSoup
import requests

import config

class CourseScraper:
    def __init__(self):
        self.university_course_pages = config.university_course_pages
        self.list_of_universities = config.list_of_universities

    def getParentURL(self, url):
        url = url[:-1]
        ind = len(url) - 1
        i = len(url) - 1

        while i >= 0:
            if url[i] == "/":
                ind = i
                break
            i = i - 1 
        
        final_url = url[:ind]
        return final_url

    def getPageURL(self, university_name):
        if university_name in self.university_course_pages.keys():
            return self.university_course_pages[university_name]
        else:
            return None

    def getPageContent(self, url):
        page_content = ""
        try:
            page_content = requests.get(url).text
        except Exception:
            page_content = ""
        return page_content

    def getSubLinks(self, page_content):
        soup = BeautifulSoup(page_content, "lxml")
        if len(soup.select('#textcontainer')) > 0:
            list_items = soup.select('#textcontainer')[0].findAll('li')
            sublinks = []

            for list_item in list_items:
                sublinks.append(list_item.findAll('a')[0]['href'])

            return sublinks

        return []
        

    def scrapeAllPages(self):
        all_sublinks = []

        for university in self.list_of_universities:
            page_content = self.getPageContent(self.getPageURL(university))
            sublinks = self.getSubLinks(page_content)
            for i in range(0, len(sublinks)):
                sublinks[i] = self.getParentURL(self.getPageURL(university)) + sublinks[i]
            all_sublinks.append(sublinks)
            break

        return all_sublinks 


if __name__ == "__main__":
    course_scraper = CourseScraper()
    all_sublinks = course_scraper.scrapeAllPages()

    for uni_link in all_sublinks:
        for link in uni_link:
            soup = BeautifulSoup(course_scraper.getPageContent(link), "lxml")
            courses = soup.find_all(class_="courseblock")
            for course in courses:
                print('-----------------------------------------')
                print(course.get_text())
                print('-----------------------------------------')
    
