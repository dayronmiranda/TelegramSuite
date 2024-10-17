from fastapi import APIRouter, HTTPException, Form
from services.telegram_client import create_session, close_session
from database.mongodb import get_db
from utils.logging import logger

router = APIRouter()

@router.post("/")
async def register_session(phone: str = Form(...), api_id: int = Form(...), api_hash: str = Form(...)):
    db = get_db()
    client = await create_session(phone, api_id, api_hash)
    try:
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            raise HTTPException(status_code=401, detail="Two-factor authentication required. Use the verify_code endpoint.")
        
        existing_session = await db.sessions.find_one({"phone": phone})
        if existing_session:
            logger.warning(f"Session already exists for number {phone}.")
            raise HTTPException(status_code=409, detail="Session already exists.")
        
        session_document = {
            "phone": phone,
            "api_id": api_id,
            "api_hash": api_hash,
            "status": "active",
            "session_data": client.session.save()
        }
        
        await db.sessions.insert_one(session_document)
        logger.info(f"Session registered successfully for {phone}")
        return {"message": "Session registered successfully."}
    except Exception as e:
        logger.error(f"Error registering session: {str(e)}")
        raise HTTPException(status_code=500, detail="Error registering session.")
    finally:
        await close_session(client)

@router.post("/verify_code")
async def verify_code(phone: str = Form(...), code: str = Form(...)):
    db = get_db()
    session_data = await db.sessions.find_one({"phone": phone})
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found. Register the session first.")
    
    client = await create_session(phone, session_data["api_id"], session_data["api_hash"])
    try:
        await client.sign_in(phone, code)
        logger.info(f"Verification code accepted for {phone}")
        return {"message": "Verification code accepted."}
    except Exception as e:
        logger.error(f"Error verifying code: {str(e)}")
        raise HTTPException(status_code=500, detail="Error verifying code.")
    finally:
        await close_session(client)