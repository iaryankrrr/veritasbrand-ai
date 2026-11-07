from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Setup Gemini (We will add your API key securely on Render later)
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

class ClaimRequest(BaseModel):
    claim: str

@app.post("/verify")
def verify_claim(req: ClaimRequest):
    guidelines = "Our brand only sells 100% organic products."
    prompt = f"Using these guidelines: {guidelines}. Verify this claim: {req.claim}. Keep it brief."
    response = model.generate_content(prompt)
    
    return {
        "claim": req.claim,
        "status": "VERIFIED" if "true" in response.text.lower() or "verified" in response.text.lower() else "REJECTED",
        "confidence": 0.9,
        "reasoning": response.text
    }
