import firebase_admin
from firebase_admin import auth, firestore, credentials

# Connect to Firebase Emulator
cred = credentials.Certificate("./service_account_key_example.json")
firebase_admin.initialize_app(cred, {
    "projectId": "demo-project"
})

# Set Firebase Emulator URLs
import os
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"

# Function to authenticate a user using the local Firebase Emulator
def authenticate_user_emulator(uid):
    user = auth.get_user(uid)
    token = auth.create_custom_token(uid)
    return {"uid": user.uid, "token": token}

# Function to fetch user data from Firestore in the Emulator
def get_user_data_emulator(uid):
    db = firestore.client()
    doc_ref = db.collection("users").document(uid)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

# Integration test with the Firebase Emulator
def test_firebase_emulator():
    # Create test user
    try:
        user = auth.create_user(uid="test-user", email="test@example.com", password="password123")
        assert user.uid == "test-user"
    except firebase_admin._auth_utils.UidAlreadyExistsError:
        pass

    # Authenticate and get a token
    result = authenticate_user_emulator("test-user")
    assert "token" in result

    # Write user data to Firestore
    db = firestore.client()
    db.collection("users").document("test-user").set({"name": "John Doe", "email": "test@example.com"})

    # Retrieve user data
    user_data = get_user_data_emulator("test-user")
    assert user_data["name"] == "John Doe"
    assert user_data["email"] == "test@example.com"

test_firebase_emulator()