# -*- coding: utf-8 -*-
"""Declare the celery tasks."""
from .extensions import celery, s3
from .email import EmailMessage
from flask import current_app


@celery.task(name="send_email")
def celery_send_email(
    id: str, email_address: str, email_title: str, api_email_link: str
) -> dict:
    """Send the reset email."""
    email_message = EmailMessage(
        user_id=id,
        email_title=email_title,
        api_email_link=api_email_link,
        email_address=email_address,
    )

    return email_message.send_message()


@celery.task(name="delete_image")
def delete_file_s3(filename):
    """Delete profile pic."""
    s3.delete_object(
        Bucket=current_app.config["S3_BUCKET"], Key=filename
    )


@celery.task(name="upload_image")
def upload_file_to_s3(filename):
    """Upload a file to S3."""
    #open filename
    opened_file = filename

    s3.upload_fileobj(opened_file, current_app.config['S3_BUCKET'], filename)

    data = f"{current_app.config['S3_LOCATION']}{filename}"
    return {"image": data}
