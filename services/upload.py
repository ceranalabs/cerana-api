import uuid
from datetime import datetime

uploads = {}

def upload_material(idea_id, file_name, file_type, file_url, file_size):
    upload_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    upload = {
        'id': upload_id,
        'ideaId': idea_id,
        'fileName': file_name,
        'fileType': file_type,
        'fileUrl': file_url,
        'fileSize': file_size,
        'uploadedAt': now
    }
    uploads[upload_id] = upload
    return upload

def delete_upload(upload_id):
    return uploads.pop(upload_id, None)
