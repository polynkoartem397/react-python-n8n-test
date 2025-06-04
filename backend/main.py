import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

from supabase_handler import add_response

app = FastAPI()
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # ✅ CORS origin
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class UserInput(BaseModel):
    message: str


@app.get("/")
async def index():
   return {"message": "Hello World"}

@app.post('/api/message')
async def message(user_input: UserInput):
    message = user_input.message
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant to summarize the context and answer the questions."},
            {"role": "user", "content": message}
        ]
    )
    print(completion.choices[0].message)
    response = completion.choices[0].message.content

    # Handle supabase
    add_response(message, response)

    # handle n8n workflow
    url = os.getenv("N8N_WEBHOOK_URL")
    data = {
        "response": response
    }
    status = requests.post(url, data)

    return response
