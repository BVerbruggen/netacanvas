import requests
import tabulate


#This file includes several functions to connect to the Canvas API and extract information

def canvas_get_students():
    #Canvas URL
    canvas_url = "https://thomasmore.instructure.com/api/v1/"

    #Request user to input token code
    print("Please generate a Canvas access token first.\nGo to https://thomasmore.instructure.com/profile/settings and use the \"New Access Code\" button to generate an access token.\nATTENTION: Be sure to set an expiration date for security reasons.")
    canvas_token = input("Please provide Canvas access token: ").strip()

    #If you want to hard-code the token, comment the previous section and uncomment the next line. Fill in your token.
    #canvas_token = "kjojoijpijoijSECRETokpk[pk["


    #Print canvas courses list
    print("##### CANVAS COURSES LIST ####")

    #Define HTTP headers
    headers = { "Authorization" : "Bearer    " + canvas_token} 

    #Return unpublishes courses as well
    body = { "include" : ["term"]}

    resp_json  = requests.get(canvas_url + "courses",headers = headers,params = body)

    resp = resp_json.json()

    course_list = [["ID","Name","Term"]]


    for course in resp:
        course_list.append([course['id'],course['name'],course['term']['name']])

    #print(resp_json.links)

    #while "next" in resp_json.links:
    while resp_json.links['current']['url'] != resp_json.links['last']['url']:
        resp_json = requests.get(resp_json.links['next']['url'], headers=headers,params = body)
        #print(resp_json.links)
        resp = resp_json.json()
        for course in resp:
            course_list.append([course['id'],course['name'],course['term']['name']])
            


    print(tabulate.tabulate(course_list, headers = "firstrow"))

    #Request user to input Canvas Course ID
    canvas_course_id = input("Provide source Canvas course ID: ")

    while not canvas_course_id.isdigit() or int(canvas_course_id) not in [i[0] for i in course_list]:
        print("Wrong input or Course ID not in course list. Try again.")
        canvas_course_id = input("Provide source Canvas course ID: ")


    #Get Canvas student enrollments

    print("##### CANVAS STUDENT ENROLLMENTS LIST ####")
    print("Getting Canvas student enrollments...")
    #Define HTTP headers
    headers = { "Authorization" : "Bearer    " + canvas_token} 

    #Only want the students, no teachers
    body = { "type" : "StudentEnrollment"}

    resp_json  = requests.get(canvas_url + "courses/" + canvas_course_id + "/enrollments?per_page=100",headers = headers, params = body)

    resp = resp_json.json()


    canvas_student_list = [["First Name","Last Name","Email Address","Student ID"]]

    for student in resp:
        if student['user']['login_id'] not in [i[2] for i in canvas_student_list]:
            name_split = student['user']['sortable_name'].split(", ", 2)
            if len(name_split) <= 1:
                name_split.append("")

            canvas_student_list.append([name_split[1],name_split[0],student['user']['login_id']])
    #print(resp_json.links)
    while "last" not in resp_json.links:

        resp_json = requests.get(resp_json.links['next']['url'], headers=headers, params = body)
        #print(resp_json.links)
        resp = resp_json.json()

        for student in resp:
            if student['user']['login_id'] not in [i[2] for i in canvas_student_list]:
                name_split = student['user']['sortable_name'].split(", ", 2)
                if len(name_split) <= 1:
                    name_split.append("")

                canvas_student_list.append([name_split[1],name_split[0],student['user']['login_id']])
    
    return canvas_student_list