from fastapi import BackgroundTasks

def write_email_log_file(message:str):
    with open("email_log.txt", mode="a") as email_file:
        email_file.write(message)

def create_log(background_tasks: BackgroundTasks, log: bool):
    if log:
        message = f"Logging email sent\n"
        background_tasks.add_task(write_email_log_file, message)

