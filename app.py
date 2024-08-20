# app.py
from flask import Flask, request, jsonify, render_template
from intents import identify_intent_and_extract_info

app = Flask(__name__,
            static_folder="../frontend/static",
            template_folder="../frontend/templates")

# Dummy data for courses and classes with IDs
courses = {
    "101": "Course 1: Introduction to Programming",
    "102": "Course 2: Data Structures",
    "103": "Course 3: Algorithms"
}
classes = {
    "201": "Class A: Math 101",
    "202": "Class B: Physics 201",
    "203": "Class C: Chemistry 301"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    intent, course_id, class_id = identify_intent_and_extract_info(user_input)

    if intent == "fetch_course":
        response = fetch_course(course_id)
    elif intent == "count_course":
        response = count_courses()
    elif intent == "fetch_class":
        response = fetch_class(class_id)
    elif intent == "count_class":
        response = count_classes()
    else:
        response = {"message": "Sorry, I don't understand that."}

    return jsonify(response)

def fetch_course(course_id):
    if course_id and course_id in courses:
        return {"message": f"Course details: {courses[course_id]}"}
    return {"message": "Course not found."}

def count_courses():
    return {"message": f"Total number of courses: {len(courses)}"}

def fetch_class(class_id):
    if class_id and class_id in classes:
        return {"message": f"Class details: {classes[class_id]}"}
    return {"message": "Class not found."}

def count_classes():
    return {"message": f"Total number of classes: {len(classes)}"}

if __name__ == '__main__':
    app.run(debug=True)
