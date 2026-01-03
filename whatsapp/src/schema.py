from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

class EmptyResponse(BaseModel):
    pass

class GreetRequest(BaseModel):
    phone_number: str
    url: str
    password: str
    

class TextMessage(BaseModel):
    body: str

class ImageMessage(BaseModel):
    id: str
    mime_type: Optional[str] = None

class AudioMessage(BaseModel):
    id: str
    url: str
    voice: str
    mime_type: Optional[str] = None

class VideoMessage(BaseModel):
    id: str
    mime_type: Optional[str] = None

class DocumentMessage(BaseModel):
    id: str
    mime_type: Optional[str] = None
    filename: Optional[str] = None

class Context(BaseModel):
    message_id: str

class Message(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: Literal["text", "image", "audio", "video", "document"]
    text: Optional[TextMessage] = None
    image: Optional[ImageMessage] = None
    audio: Optional[AudioMessage] = None
    video: Optional[VideoMessage] = None
    document: Optional[DocumentMessage] = None
    context: Optional[Context] = None

class Contact(BaseModel):
    profile: Dict[str, str]
    wa_id: str

class Metadata(BaseModel):
    phone_number_id: str
    display_phone_number: str
    verification_code: Optional[str] = None

class ChangeValue(BaseModel):
    messaging_product: Literal["whatsapp"]
    metadata: Metadata
    contacts: Optional[List[Contact]] = None
    messages: Optional[List[Message]] = None

class Value(BaseModel):
    field: str
    value: ChangeValue

class Entry(BaseModel):
    id: str
    changes: List[Value]

class WhatsappNotificationRequest(BaseModel):
    object: Literal["whatsapp_business_account"]
    entry: List[Entry]
