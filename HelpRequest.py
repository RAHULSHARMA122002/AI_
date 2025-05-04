import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")  # Update path
    firebase_admin.initialize_app(cred)

db = firestore.client()

def create_help_request(question):
    doc_ref = db.collection('helpRequests').add({
        'question': question,
        'status': 'pending',
        'createdAt': datetime.utcnow()
    })
    return doc_ref[1].id

def update_help_request(doc_id, answer):
    doc_ref = db.collection('helpRequests').document(doc_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise ValueError(f"Document with ID {doc_id} does not exist.")

    doc_ref.update({
        'answer': answer,
        'status': 'resolved',
        'resolvedAt': datetime.utcnow()
    })

def get_help_request_by_id(doc_id):
    doc = db.collection('helpRequests').document(doc_id).get()
    return doc.to_dict() if doc.exists else None

def get_pending_requests():
    return [
        {**doc.to_dict(), 'id': doc.id}
        for doc in db.collection('helpRequests').where('status', '==', 'pending').stream()
    ]

def get_resolved_requests():
    return [
        {**doc.to_dict(), 'id': doc.id}
        for doc in db.collection('helpRequests').where('status', '==', 'resolved').stream()
    ]

def get_all_help_requests():
    pending = []
    resolved = []
    docs = db.collection('helpRequests').order_by("createdAt", direction=firestore.Query.DESCENDING).stream()
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        if data["status"] == "pending":
            pending.append(data)
        else:
            resolved.append(data)
    return pending, resolved
