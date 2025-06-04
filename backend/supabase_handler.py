import os
import requests

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
api_key = os.environ.get("SUPABASE_API_KEY")

supabase_client: Client = create_client(url, api_key)

headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}


def add_response(message, response):
    data = {
        "message": message,
        "response": response
    }
    print(data)
    # user = supabase_client.auth.sign_in_with_password({ "email": "polynkoartem397", "password": "NateDev228**" })
    row = supabase_client.table("message").insert(data).execute()
    # row = supabase_client.table("message").select("*").execute()

    # # Check response status