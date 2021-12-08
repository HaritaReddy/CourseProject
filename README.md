# Course Topic Explorer: CS 410 Project (Free Topic)

### Harita Reddy (haritar2), Eric Crawford (ecraw3)

## OVERVIEW

The aim of this project was to build a comprehensive search system for students looking for the different courses that US universities are offering. We implemented a search engine with some recommendation features built based on the users’ recent search history. The major component of this project is the search feature, which the students can use to get the courses and MOOCs relevant to the keywords they enter. An advanced feature is a simple recommendation system that will recommend suitable programs that the student can apply to get knowledge on the topics they have been searching for.

## FUNCTIONALITY

The main functionalities provided by our code to the user are:
1. Search for courses from US universities. This is implemented through the functions in backend/search folder. get_relevant_courses is the function that needs to be called in order to get the relevant course documents for a given keyword query.
2. Get relevant MOOCs on Coursera offered by these universities for the searched keyword. This is implemented through the functions in backend/moocs folder. get_relevant_moocs is the function that needs to be called in order to get the relevant mooc documents for a given keyword query.
3. Recommend specific programs from different universities based on the history of keyword searches. The functions pertaining to this are implemented in backend/recommender. recommend_programs is the function that needs to be called to get the top 3 recommended programs based on the user’s search history (last three searches).

Web scraping was done once to get all the required courses. The functions are implemented in web_scraping folder.

## VIDEO TUTORIAL
https://drive.google.com/file/d/1TIVTnXw6UoFsDHuBOFQaSl5DA8uokhr6/view?usp=sharing

If the above link is not accessible, try https://mediaspace.illinois.edu/media/t/1_kis3mddw.

## INSTALLATION AND USAGE

The backend is also contained in a docker container and can be run on your local docker environment or in the cloud on any cloud provider that provides docker (pretty much all of them). The instructions below are just for running the server locally on your computer.

1. Clone the project and enter the project in your terminal.
2. Install Docker if you don’t already have it. Docker for Mac: https://docs.docker.com/desktop/mac/install/
3. Run Docker Desktop. Wait for it to go to the running mode.
4. Go to the backend folder and run docker-compose up -d. It might take a few minutes for the setup to happen, and then you should be able to go to http://localhost/main and see the site.

