from pydantic import BaseModel

class GreetRequest(BaseModel):
    phone_number: str
    password: str

class GreetResponse(BaseModel):
    status: str

class ProcessNoteRequest(BaseModel):
    phone_number: str
    base64_audio: str

class ProcessNoteResponse(BaseModel):
    status: str