from typing import Any, Dict, List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
)
from pydantic import BaseModel

from ..auth.firebase_auth import GetCurrentUserDep, get_current_user
from ..dependencies import ArtifactServiceDep
from ..models.artifact import ArtifactSource, ArtifactStatus, ArtifactType
from ..services import ArtifactService

router = APIRouter()


class ArtifactCreateRequest(BaseModel):
    message_id: str
    artifact_type: ArtifactType
    title: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ArtifactUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ArtifactStatus] = None
    content: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class ArtifactResponse(BaseModel):
    id: str
    session_id: str
    user_id: str
    message_id: str
    artifact_type: ArtifactType
    source: ArtifactSource
    title: str
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str
    status: ArtifactStatus
    content: Optional[Dict[str, Any]]
    file_path: Optional[str]
    file_size: Optional[int]
    mime_type: Optional[str]
    original_filename: Optional[str]
    storage_uri: Optional[str]
    retention_expires_at: Optional[str]
    consent_required: bool
    consent_granted: Optional[bool]

    class Config:
        from_attributes = True


class ChartArtifactRequest(BaseModel):
    message_id: str
    title: str
    chart_data: Dict[str, Any]
    description: Optional[str] = None


class ReportArtifactRequest(BaseModel):
    message_id: str
    title: str
    report_content: Dict[str, Any]
    description: Optional[str] = None


class AnalysisArtifactRequest(BaseModel):
    message_id: str
    title: str
    analysis_content: Dict[str, Any]
    description: Optional[str] = None


class FileUploadRequest(BaseModel):
    message_id: str
    title: Optional[str] = None
    description: Optional[str] = None


class ConsentRequest(BaseModel):
    artifact_id: str
    grant_consent: bool


@router.post("/{session_id}/artifacts", response_model=ArtifactResponse)
async def create_artifact(
    session_id: str,
    request: ArtifactCreateRequest,
    current_user: GetCurrentUserDep,
    artifact_service: ArtifactServiceDep,
):
    """Create a new artifact for a session"""
    try:
        user_id = current_user.uid
        artifact = await artifact_service.create_artifact(
            session_id=session_id,
            user_id=user_id,
            message_id=request.message_id,
            artifact_type=request.artifact_type,
            title=request.title,
            description=request.description,
            metadata=request.metadata,
        )
        return ArtifactResponse.model_validate(artifact)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create artifact: {str(e)}"
        )


@router.post("/{session_id}/artifacts/upload", response_model=ArtifactResponse)
async def upload_file_artifact(
    current_user: GetCurrentUserDep,
    artifact_service: ArtifactServiceDep,
    session_id: str,
    file: UploadFile = File(...),
    message_id: str = Form(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
):
    """Upload a file to create a user artifact"""
    try:
        user_id = current_user.uid

        # Read file data
        file_data = await file.read()

        artifact = await artifact_service.create_user_upload_artifact(
            session_id=session_id,
            user_id=user_id,
            message_id=message_id,
            file_data=file_data,
            filename=file.filename,
            mime_type=file.content_type,
            title=title,
            description=description,
        )

        return ArtifactResponse.model_validate(artifact)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.post("/{session_id}/artifacts/{artifact_id}/consent")
async def handle_artifact_consent(
    session_id: str,
    artifact_id: str,
    request: ConsentRequest,
    current_user: GetCurrentUserDep,
    artifact_service: ArtifactServiceDep,
):
    """Handle user consent for AI-generated artifacts"""
    try:
        user_id = current_user.uid

        if request.grant_consent:
            artifact = await artifact_service.grant_consent_for_artifact(
                artifact_id, user_id
            )
            message = "Consent granted successfully"
        else:
            artifact = await artifact_service.deny_consent_for_artifact(
                artifact_id, user_id
            )
            message = "Consent denied successfully"

        return {
            "message": message,
            "artifact": ArtifactResponse.model_validate(artifact),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to handle consent: {str(e)}"
        )


@router.get(
    "/{session_id}/artifacts/consent-required",
    response_model=List[ArtifactResponse],
)
async def get_artifacts_requiring_consent(
    session_id: str,
    current_user: GetCurrentUserDep,
    artifact_service: ArtifactServiceDep,
):
    """Get all artifacts that require user consent"""
    try:
        user_id = current_user.uid
        artifacts = await artifact_service.get_artifacts_requiring_consent(
            session_id, user_id
        )
        return [ArtifactResponse.from_orm(artifact) for artifact in artifacts]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get artifacts requiring consent: {str(e)}",
        )


@router.get(
    "/{session_id}/artifacts/source/{source}",
    response_model=List[ArtifactResponse],
)
async def get_artifacts_by_source(
    session_id: str,
    source: ArtifactSource,
    current_user: GetCurrentUserDep,
    artifact_service: ArtifactServiceDep,
):
    """Get artifacts by source (user upload or AI generated)"""
    try:
        user_id = current_user.uid
        artifacts = await artifact_service.get_artifacts_by_source(
            session_id, user_id, source
        )
        return [ArtifactResponse.from_orm(artifact) for artifact in artifacts]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get artifacts by source: {str(e)}",
        )


@router.get("/{session_id}/artifacts", response_model=List[ArtifactResponse])
async def get_session_artifacts(
    session_id: str,
    current_user: GetCurrentUserDep,
    artifact_service: ArtifactServiceDep,
):
    """Get all artifacts for a specific session"""
    try:
        user_id = current_user.uid
        artifacts = await artifact_service.get_session_artifacts(session_id, user_id)
        return [ArtifactResponse.from_orm(artifact) for artifact in artifacts]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get artifacts: {str(e)}"
        )


@router.get("/{session_id}/artifacts/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact(
    session_id: str,
    artifact_id: str,
    current_user: GetCurrentUserDep,
    artifact_service: ArtifactServiceDep,
):
    """Get a specific artifact from a session"""
    try:
        user_id = current_user.uid
        artifact = await artifact_service.get_artifact(artifact_id, user_id)
        if not artifact or artifact.session_id != session_id:
            raise HTTPException(status_code=404, detail="Artifact not found")
        return ArtifactResponse.model_validate(artifact)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get artifact: {str(e)}")


@router.put("/{session_id}/artifacts/{artifact_id}", response_model=ArtifactResponse)
async def update_artifact(
    session_id: str,
    artifact_id: str,
    request: ArtifactUpdateRequest,
    current_user: GetCurrentUserDep,
    artifact_service: ArtifactServiceDep,
):
    """Update an artifact in a session"""
    try:
        user_id = current_user.uid
        artifact = await artifact_service.update_artifact(
            artifact_id=artifact_id,
            user_id=user_id,
            title=request.title,
            description=request.description,
            status=request.status,
            content=request.content,
            metadata=request.metadata,
        )
        if not artifact or artifact.session_id != session_id:
            raise HTTPException(status_code=404, detail="Artifact not found")
        return ArtifactResponse.model_validate(artifact)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update artifact: {str(e)}"
        )


@router.delete("/{session_id}/artifacts/{artifact_id}")
async def delete_artifact(
    session_id: str,
    artifact_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete an artifact from a session"""
    try:
        user_id = current_user["uid"]
        artifact = await artifact_service.get_artifact(artifact_id, user_id)
        if not artifact or artifact.session_id != session_id:
            raise HTTPException(status_code=404, detail="Artifact not found")

        success = await artifact_service.delete_artifact(artifact_id, user_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete artifact")

        return {"message": "Artifact deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete artifact: {str(e)}"
        )


@router.post("/{session_id}/artifacts/chart", response_model=ArtifactResponse)
async def create_chart_artifact(
    session_id: str,
    request: ChartArtifactRequest,
    current_user: dict = Depends(get_current_user),
):
    """Create a chart artifact"""
    try:
        user_id = current_user["uid"]
        artifact = await artifact_service.create_chart_artifact(
            session_id=session_id,
            user_id=user_id,
            message_id=request.message_id,
            title=request.title,
            chart_data=request.chart_data,
            description=request.description,
        )
        return ArtifactResponse.from_orm(artifact)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create chart artifact: {str(e)}"
        )


@router.post("/{session_id}/artifacts/report", response_model=ArtifactResponse)
async def create_report_artifact(
    session_id: str,
    request: ReportArtifactRequest,
    current_user: dict = Depends(get_current_user),
):
    """Create a report artifact"""
    try:
        user_id = current_user["uid"]
        artifact = await artifact_service.create_report_artifact(
            session_id=session_id,
            user_id=user_id,
            message_id=request.message_id,
            title=request.title,
            report_content=request.report_content,
            description=request.description,
        )
        return ArtifactResponse.from_orm(artifact)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create report artifact: {str(e)}"
        )


@router.post("/{session_id}/artifacts/analysis", response_model=ArtifactResponse)
async def create_analysis_artifact(
    session_id: str,
    request: AnalysisArtifactRequest,
    current_user: dict = Depends(get_current_user),
):
    """Create an analysis artifact"""
    try:
        user_id = current_user["uid"]
        artifact = await artifact_service.create_analysis_artifact(
            session_id=session_id,
            user_id=user_id,
            message_id=request.message_id,
            title=request.title,
            analysis_content=request.analysis_content,
            description=request.description,
        )
        return ArtifactResponse.from_orm(artifact)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create analysis artifact: {str(e)}",
        )


@router.get(
    "/{session_id}/artifacts/type/{artifact_type}",
    response_model=List[ArtifactResponse],
)
async def get_artifacts_by_type(
    session_id: str,
    artifact_type: ArtifactType,
    current_user: dict = Depends(get_current_user),
):
    """Get artifacts by type for a specific session"""
    try:
        user_id = current_user["uid"]
        artifacts = await artifact_service.get_artifacts_by_type(
            session_id, user_id, artifact_type
        )
        return [ArtifactResponse.from_orm(artifact) for artifact in artifacts]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get artifacts by type: {str(e)}",
        )


@router.get(
    "/{session_id}/artifacts/status/{status}", response_model=List[ArtifactResponse]
)
async def get_artifacts_by_status(
    session_id: str,
    status: ArtifactStatus,
    current_user: dict = Depends(get_current_user),
):
    """Get artifacts by status for a specific session"""
    try:
        user_id = current_user["uid"]
        artifacts = await artifact_service.get_artifacts_by_status(
            session_id, user_id, status
        )
        return [ArtifactResponse.from_orm(artifact) for artifact in artifacts]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get artifacts by status: {str(e)}",
        )


@router.get(
    "/{session_id}/messages/{message_id}/artifacts",
    response_model=List[ArtifactResponse],
)
async def get_message_artifacts(
    session_id: str,
    message_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Get all artifacts for a specific message"""
    try:
        user_id = current_user["uid"]
        artifacts = await artifact_service.get_message_artifacts(message_id, user_id)
        # Filter to ensure all artifacts are from the same session
        session_artifacts = [art for art in artifacts if art.session_id == session_id]
        return [ArtifactResponse.from_orm(artifact) for artifact in session_artifacts]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get message artifacts: {str(e)}"
        )


@router.put("/{session_id}/artifacts/{artifact_id}/status")
async def update_artifact_status(
    session_id: str,
    artifact_id: str,
    status: ArtifactStatus,
    current_user: dict = Depends(get_current_user),
):
    """Update artifact status"""
    try:
        user_id = current_user["uid"]
        artifact = await artifact_service.get_artifact(artifact_id, user_id)
        if not artifact or artifact.session_id != session_id:
            raise HTTPException(status_code=404, detail="Artifact not found")

        success = await artifact_service.update_artifact_status(
            artifact_id, user_id, status
        )
        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to update artifact status"
            )

        return {"message": "Artifact status updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update artifact status: {str(e)}"
        )


@router.get("/artifacts", response_model=List[ArtifactResponse])
async def get_user_artifacts(
    limit: Optional[int] = Query(None, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    """Get all artifacts for the current user across all sessions"""
    try:
        user_id = current_user["uid"]
        artifacts = await artifact_service.get_user_artifacts(user_id, limit)
        return [ArtifactResponse.from_orm(artifact) for artifact in artifacts]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get user artifacts: {str(e)}"
        )
