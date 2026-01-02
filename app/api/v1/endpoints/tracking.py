from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.nlp import voice_parser

router = APIRouter()

class VoiceLogInput(BaseModel):
    transcript: str

@router.post("/log-voice")
def log_food_by_voice(data: VoiceLogInput):
    if not data.transcript:
        raise HTTPException(status_code=400, detail="Transcript empty")
        
    result = voice_parser.parse_voice_log(data.transcript)
    return result