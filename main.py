from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os
from dotenv import load_dotenv


load_dotenv()


API_KEYS_CREDITS = {
    os.getenv("API_KEY"): 5
}


app = FastAPI()


def verify_token_api_key(api_key_input: str = Header(None)):
    credits = API_KEYS_CREDITS.get(api_key_input, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid Api key, or no credits")

    return api_key_input


@app.post("/generate")
def generate(prompt: str, api_key: str = Depends(verify_token_api_key)):
    API_KEYS_CREDITS[api_key] -= 1
    responseLlm = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return {"response": responseLlm["message"]["content"]}


