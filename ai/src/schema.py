from pydantic import BaseModel

class AnonymizeRequest(BaseModel):
    text: str

class STTRequest(BaseModel):
    base64_audio: str