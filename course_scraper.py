from bs4 import BeautifulSoup
import requests
import pickle

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
                if len(list_item.findAll('a')) > 0:
                    sublinks.append(list_item.findAll('a')[0]['href'])

            return sublinks

        return []
        

    def scrapeAllPages(self):
        all_universities_courses = {}

        for university in self.list_of_universities:
            all_universities_courses[university] = []
            page_content = self.getPageContent(self.getPageURL(university))
            sublinks = self.getSubLinks(page_content)
            for i in range(0, len(sublinks)):
                sublinks[i] = self.getParentURL(self.getPageURL(university)) + sublinks[i]
            
            for sublink in sublinks:
                soup = BeautifulSoup(course_scraper.getPageContent(sublink), "lxml")
                courses = soup.find_all(class_="courseblock")
                for course in courses:
                    all_universities_courses[university].append(course.get_text() + ' ' + sublink)

        return all_universities_courses


if __name__ == "__main__":
    course_scraper = CourseScraper()
    all_universities_courses = course_scraper.scrapeAllPages()

    print(all_universities_courses['CMU'])
    print(all_universities_courses['UIUC'])

    with open('all_universities_courses.pickle', 'wb') as handle:
        pickle.dump(all_universities_courses, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
