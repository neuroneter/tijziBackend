
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.otp import OTPService
from app.services.whatsapp import send_whatsapp_message
from app.config import settings

auth_router = APIRouter()
otp_service = OTPService()

class SendCodeRequest(BaseModel):
    phone_number: str

class VerifyCodeRequest(BaseModel):
    phone_number: str
    code: str

@auth_router.post("/send-code")
def send_code(request: SendCodeRequest):
    code = otp_service.generate_and_store_code(request.phone_number)
    success = send_whatsapp_message(request.phone_number, code)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message.")
    return {"message": "Code sent successfully"}

@auth_router.post("/verify-code")
def verify_code(request: VerifyCodeRequest):
    if otp_service.verify_code(request.phone_number, request.code):
        return {"token": otp_service.generate_token(request.phone_number)}
    raise HTTPException(status_code=401, detail="Invalid code")
