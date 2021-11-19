from bs4 import BeautifulSoup
import requests
import pickle

import config

class ProgramScraper:
    def __init__(self):
        self.university_program_pages = config.university_program_pages
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
        if university_name in self.university_program_pages.keys():
            return self.university_program_pages[university_name][0]
        else:
            return None

    def getPageContent(self, url):
        page_content = ""
        try:
            page_content = requests.get(url).text
        except Exception:
            page_content = ""
        return page_content

    def getSublinkClassOrID(self, university_name):
        if university_name in self.university_program_pages.keys():
            return self.university_program_pages[university_name][1]
        else:
            return None

    def getContentClassOrID(self, university_name):
        if university_name in self.university_program_pages.keys():
            return self.university_program_pages[university_name][2]
        else:
            return None

    def getSubLinks(self, page_content, classoridname):
        soup = BeautifulSoup(page_content, "lxml")
        
        if len(soup.find("div", classoridname)) > 0:
            list_items = soup.find("div", classoridname).findAll('a', href=True)
            sublinks = []

            for list_item in list_items:
                sublinks.append(list_item['href'])

            return sublinks

        return []
        

    def scrapeAllPages(self):
        all_universities_programs = {}

        for university in self.list_of_universities:
            if university not in self.university_program_pages:
                continue
            all_universities_programs[university] = []
            page_content = self.getPageContent(self.getPageURL(university))

            sublinks = self.getSubLinks(page_content, self.getSublinkClassOrID(university))
            for i in range(0, len(sublinks)):
                sublinks[i] = self.getParentURL(self.getPageURL(university)) + sublinks[i]

            if university == "GATECH":
                for sublink in sublinks:
                    print(sublink)
                    soup = BeautifulSoup(self.getPageContent(sublink), "lxml")
                    complete_program_content = soup.findAll("title")[0].get_text() + ": "
                    if soup.find("div", self.getContentClassOrID(university)) == None:
                        continue
                    program_content = soup.find("div", self.getContentClassOrID(university)).findAll('p')

                    for item in program_content:
                        complete_program_content = complete_program_content + item.get_text()

                    print(complete_program_content)
                    all_universities_programs[university].append(complete_program_content + ' ' + sublink)
            elif university == "UIUC":
                for sublink in sublinks:
                    soup = BeautifulSoup(self.getPageContent(sublink), "lxml")
                    complete_program_content = soup.findAll("title")[0].get_text() + ": "
                    complete_program_content = complete_program_content + soup.findAll('p')[1].get_text()
                    print(complete_program_content)
                    all_universities_programs[university].append(complete_program_content + ' ' + sublink)
            
        return all_universities_programs


if __name__ == "__main__":
    program_scraper = ProgramScraper()
    all_universities_programs = program_scraper.scrapeAllPages()
    #print(all_universities_programs["UIUC"])
   
    with open('program_catalogs/GATECH.pickle', 'wb') as handle:
        pickle.dump(all_universities_programs['GATECH'], handle, protocol=pickle.HIGHEST_PROTOCOL)
    

    with open('program_catalogs/UIUC.pickle', 'wb') as handle:
        pickle.dump(all_universities_programs['UIUC'], handle, protocol=pickle.HIGHEST_PROTOCOL)
   