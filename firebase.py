# knowledge_base.py

import os
import json
from datetime import datetime
from fuzzywuzzy import fuzz, process
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase init
if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")  
    firebase_admin.initialize_app(cred)

db = firestore.client()
print("hello firebase")
file_path = os.path.join(os.path.dirname(__file__), "knowledge_base.json")

# Load local file
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        knowledge_base = json.load(f)
else:
    knowledge_base = {}

def find_answer(query):
    query = query.lower()
    questions = list(knowledge_base.keys())

    if not questions:
        return None

    best_match, score = process.extractOne(query, questions, scorer=fuzz.ratio)
    if score > 70:
        return knowledge_base[best_match]
    return None

def update_knowledge_base(question, answer):
    question = question.lower()
    knowledge_base[question] = answer

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, indent=2)

    db.collection("knowledgeBase").add({
        "question": question,
        "answer": answer,
        "createdAt": datetime.utcnow()
    })
