import cPickle as pickle
import os

path = 'program_catalogs/'
files = os.listdir(path)

course_list = []


for file in files:
    print(file)
    with (open(path + file, "rb")) as openfile:
        university_courses = pickle.load(openfile)
        for course in university_courses:
            course_list.append(course.replace('\n', ' '))


#dat_file = open("courses.dat", "w")
dat_file = open("programs.dat", "w")
for element in course_list:
    dat_file.write(element.encode('utf-8') + "\n")

dat_file.close()