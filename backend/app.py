# app.py
from flask import Flask, request, jsonify, render_template
import requests  # Import the requests library
from intents import identify_intent_and_extract_info

app = Flask(__name__,
            static_folder="../frontend/static",
            template_folder="../frontend/templates")

# Replace with your actual API endpoints
SABA_CERTIFICATE = "?SabaCertificate=UUEwMDNeI14xY19sMmhnLTZ4X2hsUXZvTHpZVXVMVDZHQWcwQWJrN2Nsc2lOdFFCNU5CRkg4VU1JUHAtd0VEcGN1V2lZaS1FcXFNZ2hDYUR6MzQtQmtMM1d5YmZMN2hWNUlzRkpZNHUxdWp4WG54S2pBTTlleUxMOGRZR0tXMG0zTDJhbG5rdE9YNGFLcDNCV3NreEU2WUtlazhoNk4zQjVLaXVWbUh6NmVlMjdDTERGVHc"
COURSE_API_BASE_URL = "https://dq3qa003-api.sabacloud.com/v1/course"
CLASS_API_BASE_URL = "https://dq3qa003-api.sabacloud.com/v1/offering"
COURSE_COUNT_API_URL = "http://api.example.com/courses/count"
CLASS_COUNT_API_URL = "http://api.example.com/classes/count"
COURSE_REDIRECT_URL = "https://dq3qa003.sabacloud.com/Saba/Web_wdk/QA003Admin/learning/learningoffering/offeringTemplate/offeringTemplateDetail.rdf?id="

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    intent, course_id, class_id = identify_intent_and_extract_info(user_input)

    start_message = "Sure. Please find below result/s as for : "

    if intent == "fetch_course":
        start_message = f"{start_message}{course_id}<br><br>"
        response = fetch_course(course_id,start_message)
    elif intent == "count_course":
        start_message = f"{start_message}{course_id}<br><br>"
        response = count_courses()
    elif intent == "fetch_class":
        start_message = f"{start_message}{class_id}<br><br>"
        response = fetch_class(class_id,start_message)
    elif intent == "count_class":
        start_message = f"{start_message}{class_id}<br><br>"
        response = count_classes()
    else:
        response = {"message": "Sorry, I don't understand that."}

    print(response)
    return jsonify(response)

def fetch_course(course_id,start_message):
    if course_id:
        try:
            print(f"{COURSE_API_BASE_URL}/{course_id}{SABA_CERTIFICATE}")
            response = requests.get(f"{COURSE_API_BASE_URL}/{course_id}{SABA_CERTIFICATE}")
            if response.status_code == 200:
               data = response.json()
               # Extract specific attributes from the JSON
               course_name = data.get("title","N/A")
               print(course_name)
               course_description = data.get("description","No description available.")
               print(course_description)
               link = f"{COURSE_REDIRECT_URL}{course_id}"
               if not course_description:
                return (f"{start_message}<br>Course title : <b>{course_name}</b> <br><br> redirect link - <a href='{link}' target='_blank'> Click ME ! </a>")
               else:
                return (f"{start_message}<br>Course title : <b>{course_name}</b> <br><br> Course description : <br> <b>{course_description}</b> <br><br> Redirect Link - <a href='{link}' target='_blank'> Click ME ! </a>")
            else:
                return {"message": "Course not found or API error."}
        except Exception as e:
            return {"message": f"Error fetching course: {str(e)}"}
    return {"message": "Course ID not provided."}

def count_courses():
    try:
        response = requests.get(COURSE_COUNT_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {"message": "Error fetching course count."}
    except Exception as e:
        return {"message": f"Error fetching course count: {str(e)}"}

def fetch_class(class_id,start_message):
    if class_id:
        try:
            print(f"{CLASS_API_BASE_URL}/{class_id}{SABA_CERTIFICATE}")
            response = requests.get(f"{CLASS_API_BASE_URL}/{class_id}{SABA_CERTIFICATE}")
            if response.status_code == 200:
               data = response.json()
               # Extract specific attributes from the JSON
               class_title = data.get("title","N/A")
               print(class_title)
               class_description = data.get("description","No description available.")
               print(class_description)
               return (f"{start_message}Class title is {class_title} and Course description is {class_description}")
            else:
                return {"message": "Class not found or API error."}
        except Exception as e:
            return {"message": f"Error fetching class: {str(e)}"}
    return {"message": "Class ID not provided."}

def count_classes():
    try:
        response = requests.get(CLASS_COUNT_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {"message": "Error fetching class count."}
    except Exception as e:
        return {"message": f"Error fetching class count: {str(e)}"}

if __name__ == '__main__':
    app.run(debug=True)
