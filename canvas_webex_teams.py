import requests
import json
from canvas_utils import canvas_get_students

#API info
access_token = 'opkopkpokpokpokpokpSECRETlml;kkpok'
url = 'https://webexapis.com/v1/'

#HTTP Headers
headers = {
 'Authorization': 'Bearer {}'.format(access_token)
}

#Get Teams list
res = requests.get(url + "teams", headers=headers)
print(json.dumps(res.json(), indent=4))

#Get Webex Team ID to add users to
team_id = input("Input team ID:")

#Get student enrollments from Canvas
student_list = canvas_get_students()

#Add student emails to Webex Team
for email in [row[2] for row in student_list[1:]]:

    print("####Adding " + email + " to Webex Team... ####")
    body = {
        'teamId' : team_id,
        'personEmail' : email,
        'isModerator' : False
    }
    res = requests.post(url + "team/memberships", headers=headers, data =  body)
    print(json.dumps(res.json(), indent=4))