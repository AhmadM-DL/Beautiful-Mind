from pydantic import BaseModel

class GreetRequest(BaseModel):
    phone_number: str
    password: str
    url: str

class EmptyResponse(BaseModel):
    pass

class ProcessNoteRequest(BaseModel):
    phone_number: str
    base64_audio: str
