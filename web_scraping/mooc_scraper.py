from bs4 import BeautifulSoup
import requests
import pickle

import config

class MOOCScraper:
    def __init__(self):
        self.mooc_pages = [('UCI', 'https://www.coursera.org/uci'), ('UCB', 'https://www.coursera.org/boulder'), ('GATECH', 'https://www.coursera.org/gatech')]
        #[('UIUC', 'https://www.coursera.org/illinois'), ('GATECH', 'https://www.coursera.org/gatech')]

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
        list_items = soup.findAll('a')
        sublinks = []

        for list_item in list_items:
            sublinks.append(list_item['href'])

        
        return sublinks
        

    def scrapeAllPages(self):
        all_universities_moocs = {}

        for university_page in self.mooc_pages :
            page_content = self.getPageContent(university_page[1])
            sublinks = self.getSubLinks(page_content)
            #print(page_content)
            #print(sublinks)

            filtered_sublinks = []

            for i in range(0, len(sublinks)):
                if '/learn/' in sublinks[i]:
                    filtered_sublinks.append('https://www.coursera.org' + sublinks[i])
            
            print(filtered_sublinks)

            all_universities_moocs[university_page[0]] = []

            for sublink in filtered_sublinks:
                soup = BeautifulSoup(self.getPageContent(sublink), "lxml")
                title_block = soup.find_all("title")
                if len(title_block) == 0:
                    continue
                title = title_block[0].get_text()
                desc_block = soup.find_all(class_="content-inner")
                if len(desc_block) == 0:
                    continue
                description = desc_block[0].get_text().strip().replace('  ', ' ').replace('\n', ' ')
                text_item = title + ' ' + description + ' ' + university_page[1]

                print("Completed for " + title)

                all_universities_moocs[university_page[0]].append(text_item)

        return all_universities_moocs


if __name__ == "__main__":
    mooc_scraper = MOOCScraper()
    all_universities_moocs = mooc_scraper.scrapeAllPages()
    with open('mooc_list.dat', 'a') as file:
        for key, value in all_universities_moocs.items():
            for item in value:
                try:
                    file.write(item.encode('utf-8') + '\n')
                except UnicodeEncodeError:
                    continue