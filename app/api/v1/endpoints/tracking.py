# app/api/v1/endpoints/tracking.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.nlp import voice_parser

router = APIRouter()

class VoiceLogInput(BaseModel):
    transcript: str # The text converted from speech by the mobile app

@router.post("/log-voice")
def log_food_by_voice(data: VoiceLogInput):
    """
    Receives text transcript from App, returns structured Food JSON.
    """
    if not data.transcript:
        raise HTTPException(status_code=400, detail="Transcript empty")
        
    result = voice_parser.parse_voice_log(data.transcript)
    return result