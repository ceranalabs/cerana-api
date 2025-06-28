from flask import Blueprint, request, jsonify
from schemas.upload import UploadedMaterial
from services import upload as upload_service
from utils.auth import require_auth

bp = Blueprint('uploads', __name__)

@bp.route('/uploads', methods=['POST'])
@require_auth
def upload():
    # For MVP, simulate upload (no real file storage)
    idea_id = request.form.get('ideaId')
    file_type = request.form.get('fileType')
    file = request.files.get('file')
    if not file or not idea_id or not file_type:
        return jsonify({'error': 'Missing file, ideaId, or fileType'}), 400
    file_name = file.filename
    file_url = f"https://fake-storage/{file_name}"
    file_size = len(file.read())
    upload = upload_service.upload_material(idea_id, file_name, file_type, file_url, file_size)
    return jsonify(UploadedMaterial(**upload).model_dump(mode="json")), 201

@bp.route('/uploads/<upload_id>', methods=['DELETE'])
@require_auth
def delete_upload(upload_id):
    deleted = upload_service.delete_upload(upload_id)
    if not deleted:
        return '', 404
    return '', 204
