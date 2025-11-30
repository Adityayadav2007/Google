from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from agents.education_agent import EducationAgent
from agents.health_agent import HealthcareAgent
from agents.sustain_agent import SustainabilityAgent

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print("API KEY LOADED:", API_KEY)


app = FastAPI()

edu = EducationAgent(API_KEY)
health = HealthcareAgent(API_KEY)
sustain = SustainabilityAgent(API_KEY)

class Prompt(BaseModel):
    prompt: str

@app.post("/agent/education")
def ask_education(p: Prompt):
    return {"response": edu.run(p.prompt)}

@app.post("/agent/healthcare")
def ask_health(p: Prompt):
    return {"response": health.run(p.prompt)}

@app.post("/agent/sustainability")
def ask_sustain(p: Prompt):
    return {"response": sustain.run(p.prompt)}

@app.get("/")
def root():
    return {"message": "Agents for Good API running"}

