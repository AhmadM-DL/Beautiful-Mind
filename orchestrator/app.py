from src.config import AI_SERVICE_URL, BACKEND_SERVICE_URL
from src.schema import GreetRequest, ProcessNoteRequest, GreetResponse, ProcessNoteResponse 
from src.orchestration_service import orchestration_service
from src.meta_service import meta_service
from src.greeting_service import greeting_service
from fastapi import FastAPI, HTTPException, BackgroundTasks
import requests, os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Orchestrator Service")

@app.post("/greet_patient", response_model=GreetResponse)
async def greet_patient(request: GreetRequest):
    try:
        meta_service.send_message(request.phone_number, greeting_service.greeting_msg)
    except Exception as e:
        logger.error(f"Error greeting patient: {e}")
        raise HTTPException(status_code=500)
    return GreetResponse(status="success")

@app.post("/process_patient_note", response_model=ProcessNoteResponse)
async def process_patient_note(request: ProcessNoteRequest, background_tasks: BackgroundTasks):
    try:
        token = orchestration_service.login_by_phone(request.phone_number)
    except Exception as e:
        logger.error(f"Error logging in: {e}")
        raise HTTPException(status_code=401)
    background_tasks.add_task(orchestration_service.process_voice_note, token, request.base64_audio)
    return ProcessNoteResponse(status="success")

