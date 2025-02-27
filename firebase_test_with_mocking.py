from unittest.mock import patch, MagicMock
import firebase_admin
from firebase_admin import auth, firestore, credentials

# Initialize Firebase app (mocked in tests)
cred = credentials.Certificate("./service_account_key_example.json")
firebase_admin.initialize_app(cred)

# Function to authenticate a user and retrieve an ID token
def authenticate_user(uid):
    user = auth.get_user(uid)
    token = auth.create_custom_token(uid)
    return {"uid": user.uid, "token": token}

# Function to fetch a document from Firestore
def get_user_data(uid):
    db = firestore.client()
    doc_ref = db.collection("users").document(uid)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

# Unit test with mocks
@patch("firebase_admin.auth.get_user")
@patch("firebase_admin.auth.create_custom_token")
@patch("firebase_admin.firestore.client")
def test_authenticate_user(mock_firestore, mock_create_token, mock_get_user):
    # Mock user data
    mock_get_user.return_value = MagicMock(uid="12345")
    mock_create_token.return_value = "fake-token"
    
    result = authenticate_user("12345")
    assert result["uid"] == "12345"
    assert result["token"] == "fake-token"

@patch("firebase_admin.firestore.client")
def test_get_user_data(mock_firestore):
    # Mock Firestore response
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {"name": "John Doe", "email": "john@example.com"}
    mock_firestore.return_value.collection.return_value.document.return_value.get.return_value = mock_doc

    result = get_user_data("12345")
    assert result["name"] == "John Doe"
    assert result["email"] == "john@example.com"