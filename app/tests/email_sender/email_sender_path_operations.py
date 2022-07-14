from fastapi import APIRouter, BackgroundTasks
from utilities.email_sender import email_sender

router = APIRouter(
    prefix='/test',
    tags=['Tests']
)

@router.get('/send-email/asynchronous')
async def send_email_asynchronous():
    await email_sender.send_email_async('Hello World','mohamedamine.benammar@etudiant-isi.utm.tn',
    {'title': 'Hello World', 'name': 'John Doe'})
    return 'Success'

@router.get('/send-email/backgroundtasks')
def send_email_backgroundtasks(background_tasks: BackgroundTasks):
    email_sender.send_email_background(background_tasks, 'Hello World',   
    'mohamedamine.benammar@etudiant-isi.utm.tn', {'title': 'Hello World', 'name': 'John Doe'})
    return 'Success'