from src.schema import GreetRequest, ProcessNoteRequest, EmptyResponse 
from src.orchestration_service import orchestration_service
from src.meta_service import meta_service
from fastapi import FastAPI, HTTPException, BackgroundTasks
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Orchestrator Service")

@app.post("/greet_patient", response_model=EmptyResponse)
async def greet_patient(request: GreetRequest):
    try:
        meta_service.greet_patient(request.phone_number, request.password, request.url)
    except Exception as e:
        logger.error(f"Error greeting patient: {e}")
        raise HTTPException(status_code=500)
    return EmptyResponse()

@app.post("/process_patient_note", response_model=EmptyResponse)
async def process_patient_note(request: ProcessNoteRequest, background_tasks: BackgroundTasks):
    try:
        token = orchestration_service.login_by_phone(request.phone_number)
    except Exception as e:
        logger.error(f"Error logging in: {e}")
        raise HTTPException(status_code=401)
    background_tasks.add_task(orchestration_service.process_voice_note, token, request.base64_audio)
    return EmptyResponse()

