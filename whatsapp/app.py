from fastapi import FastAPI, HTTPException, Response, Depends, status, Query
from src.schema import WhatsappNotificationRequest, EmptyResponse, GreetRequest
from src.config import META_HANDSHAKE_SECRET
from src.meta_service import meta_service
from src.orchestrator_service import orchestrator_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI(title="WhatsApp Service")

def token_bearer(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    if not token == META_HANDSHAKE_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token

@app.post("/greet_patient", response_model=EmptyResponse)
def greet_patient(request: GreetRequest, token: str = Depends(token_bearer)):
    try:
        meta_service.send_template_message(request.phone_number, "greet_patient", "ar", {"domain": request.url})
        meta_service.send_template_message(request.phone_number, "share_password", "ar", {"password": request.password})
        return EmptyResponse()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/webhook", response_model=EmptyResponse)
def webhook(notificaion: WhatsappNotificationRequest):
    # Is message notification
    try:
        message = notificaion.entry[0].changes[0].value.messages[0]
    except Exception as e:
        return EmptyResponse()
    # Is voice note
    if message.type == "audio" and message.audio.voice == "true":
        audio_url = message.audio.url
        try:
            base64_audio = meta_service.get_media_as_base64(audio_url)
            orchestrator_service.process_voice_note(message.from_, base64_audio)
        except Exception as e:
            return EmptyResponse()
        try:
            meta_service.send_thumbs_up(message.from_, message.id)
        except Exception as e:
            return EmptyResponse()
    return EmptyResponse()


@app.get("/webhook")
def webhook_handshake(
    mode: str = Query(None, alias="hub.mode"),
    verify_token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if mode == "subscribe" and verify_token == META_HANDSHAKE_SECRET:
        return Response(content=challenge)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        

