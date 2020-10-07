import csv
from canvas_utils import canvas_get_students


student_list = canvas_get_students()
#Write to students.csv file
print("Writing students to students.csv...")    
f = open('students.csv', 'w', newline='')

with f:

    writer = csv.writer(f)
    writer.writerows(student_list)
print("Done! Please doublecheck and upload the students.csv file to your Netacad course.")



