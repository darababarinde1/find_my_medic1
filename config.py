import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'darababarinde4@gmail.com',
    'sender_password': 'llkd weqc diov oevs',
    'recipient_email': 'coding-challenges+clin-alerts@sprinterhealth.com'
}

API_BASE_URL = 'https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test'
CLINICIAN_IDS = [1, 2, 3, 4, 5, 6, 7]
POLLING_INTERVAL = 60  
