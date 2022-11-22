from flask import current_app
from werkzeug.utils import secure_filename
import os
from ...tasks import upload_file_to_s3


def allowed_file(filename: str) -> bool:
    """Check if the file is allowed."""
    allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def upload_image(file):
    """Upload image to S3."""
    if not file:
        raise ValueError("The file has to be provided!")
    if file.filename == "":
        raise ValueError("The file has to be provided!")
    if not allowed_file(file.filename):
        raise TypeError("That file type is not allowed!")

    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    # upload_file_to_s3.delay(filename)
    upload_file_to_s3(filename)

    profile_pic = f"{current_app.config['S3_LOCATION']}{filename}"

    return profile_pic


def handle_upload_image(file):
    """Handle image upload."""
    try:
        profile_pic = upload_image(file)
    except (ValueError, TypeError) as e:
        raise e
    except Exception as e:
        raise e
    else:
        return profile_pic