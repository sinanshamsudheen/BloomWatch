from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
from services.chat_service import chat_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatQuery(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.on_event("startup")
async def startup_event():
    """Initialize the chat service on startup"""
    logger.info("Initializing chat service...")
    success = chat_service.initialize()
    if success:
        logger.info("Chat service initialized successfully")
    else:
        logger.warning("Failed to initialize chat service")

@router.post("/chat", response_model=ChatResponse)
async def chat(query: ChatQuery):
    """Get a response to a chat query using RAG"""
    try:
        response = chat_service.get_response(query.message)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing chat query: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat query")

@router.get("/chat/status")
async def chat_status():
    """Check if the chat service is available"""
    return {"initialized": chat_service.is_initialized}