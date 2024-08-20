# intents.py
import spacy
import re
from spacy.matcher import PhraseMatcher

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Define phrases for intents
phrases = {
    "fetch_course": [
        "fetch course", "get course", "retrieve course", "show course",
        "find course", "look up course", "course information",
        "course details", "display course", "course data"
    ],
    "count_course": [
        "count course", "number of courses", "total courses",
        "how many courses", "course count", "courses available",
        "count of courses", "number of available courses"
    ],
    "fetch_class": [
        "fetch class", "get class", "retrieve class", "show class",
        "find class", "look up class", "class information",
        "class details", "display class", "class data"
    ],
    "count_class": [
        "count class", "number of classes", "total classes",
        "how many classes", "class count", "classes available",
        "count of classes", "number of available classes"
    ],
    "create_course": [
        "create a course", "develop a course", "generate a course", "create a java course", "Create a new course",
        "develop a new course", "generate a new course", "Build a new course", "create course", "develop course", "generate course", "make course"
        "Start a new course", "Set up a new course", "Build a course", "Create a training course", "Can you help me create a course?"
    ],
    "assign_course_to_all": [
        "assign course java to all", "assign course to all", "assign course to everyone", ""
    ]
}

# Add phrases to the matcher
for intent, phrase_list in phrases.items():
    patterns = [nlp.make_doc(text) for text in phrase_list]
    matcher.add(intent, patterns)

def identify_intent_and_extract_info(user_input):
    doc = nlp(user_input)
    matches = matcher(doc)

    if matches:
        match_id, start, end = matches[0]  # Take the first match
        intent = nlp.vocab.strings[match_id]

        # Extract ID or unique field if applicable
        course_id = None
        class_id = None
        course_title = None

        if intent in ["fetch_course", "fetch_class", "create_course", "assign_course_to_all"]:
            # Example of extracting an ID from a string like "course ID 123"
            course_id_match = re.search(r'course\sID\s(\w+)', user_input, re.IGNORECASE)
            if course_id_match:
                course_id = course_id_match.group(1)

            class_id_match = re.search(r'class\sID\s(\w+)', user_input, re.IGNORECASE)
            if class_id_match:
                class_id = class_id_match.group(1)

            course_title_match = re.search(r'course\sTitle\s(\w+)', user_input, re.IGNORECASE)
            if course_title_match:
                course_title = course_title_match.group(1)    

        return intent, course_id, class_id, course_title

    return "unknown", None, None
