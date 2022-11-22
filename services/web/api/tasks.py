# -*- coding: utf-8 -*-
"""Declare the celery tasks."""
from .extensions import celery, s3
from .email import EmailMessage
from flask import current_app
import os


# @celery.task(name="send_email")
def celery_send_email(
    id: str, email_address: str, email_title: str, api_email_link: str, role: str
) -> dict:
    """Send the reset email."""
    email_message = EmailMessage(
        user_id=id,
        email_title=email_title,
        api_email_link=api_email_link,
        email_address=email_address,
        role=role
    )

    return email_message.send_message()


# @celery.task(name="delete_image")
def delete_file_s3(filename):
    """Delete profile pic."""
    s3.delete_object(
        Bucket=current_app.config["S3_BUCKET"], Key=filename
    )


# @celery.task(name="upload_image")
def upload_file_to_s3(filename):
    """Upload a file to S3."""

    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'rb') as profilepic:
        print('Loaded the file')
        # s3.upload_fileobj(profilepic, current_app.config['S3_BUCKET'], filename, ExtraArgs={'ACL': 'public-read'})
        s3.upload_fileobj(profilepic, current_app.config['S3_BUCKET'], filename)
        os.remove(filepath)

    data = f"{current_app.config['S3_LOCATION']}{filename}"
    return {"image": data}
