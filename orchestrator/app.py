from src.config import AI_SERVICE_URL, BACKEND_SERVICE_URL
from src.schema import GreetRequest, ProcessNoteRequest, GreetResponse, ProcessNoteResponse 
from src.orchestration_service import orchestration_service
from fastapi import FastAPI, HTTPException
import requests, os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Orchestrator Service")

@app.post("/greet_patient")
async def greet_patient(request: GreetRequest)-> GreetResponse:
    return {"status": "success"}

@app.post("/process_patient_note")
async def process_patient_note(request: ProcessNoteRequest)-> ProcessNoteResponse:
    try:
        orchestration_service.process_voice_note(request.phone_number, request.base64_audio)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing voice note: {e}")
        raise HTTPException(status_code=500)

