from fastapi import FastAPI
from pydantic import BaseModel
import SOP 
from crewai import Crew, Process, Task
import os

app = FastAPI()

class SOPInput(BaseModel):
    marketing_txt: str

@app.get("/")
def home():
    return {"status": "Serveur S&OP Cloud Actif"}

@app.post("/analyser")
async def run_analysis(data: SOPInput):
    # On récupère la clé Groq depuis l'environnement du serveur
    api_key = os.getenv("GROQ_API_KEY")
    
    # On définit les tâches
    t1 = Task(description=f"Analyse Demande: {data.marketing_txt}", agent=SOP.marketing, expected_output="Rapport")
    t6 = Task(description="Rapport Final PIC complet en français", agent=SOP.orchestrator, expected_output="Plan")

    crew = Crew(
        agents=[SOP.marketing, SOP.sales, SOP.supply, SOP.purchasing, SOP.finance, SOP.orchestrator],
        tasks=[t1, t6],
        process=Process.sequential
    )

    resultat = crew.kickoff()
    return {"plan_final": str(resultat)}
