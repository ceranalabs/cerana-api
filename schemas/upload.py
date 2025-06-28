from pydantic import BaseModel, HttpUrl

class UploadedMaterial(BaseModel):
    id: str
    ideaId: str
    fileName: str
    fileType: str
    fileUrl: HttpUrl
    fileSize: int
    uploadedAt: str
