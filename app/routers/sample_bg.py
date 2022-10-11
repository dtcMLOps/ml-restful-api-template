from fastapi import BackgroundTasks
from app.services.sample_bg_crud import write_email_log_file, create_log
from fastapi import APIRouter, Depends, Query


router = APIRouter(prefix="/bg_task")

@router.post("/send-email-with-log/{email_id}")
async def send_email_with_log(email_id: str, background_tasks: BackgroundTasks, log: bool = Depends(create_log)):
    message = f"Hello, World to {email_id}\n"
    background_tasks.add_task(write_email_log_file, message) 
    return {"message": "Email sent"}
