# Enhanced Artifact System

The enhanced artifact system supports both user-uploaded files and AI-generated artifacts with proper consent management and clear distinction between sources.

## Features

### 🔄 Dual Source Support

- **User Uploads**: PDF, CSV, images, documents, spreadsheets
- **AI Generated**: Charts, reports, analyses, visualizations, recommendations

### 🔒 Consent Management

- AI-generated artifacts require user consent if not globally granted
- User uploads have implicit consent (no additional consent needed)
- Per-artifact consent granting/denial
- Global consent settings for automatic approval

### 📁 File Management

- Secure file storage with unique naming
- File type detection and validation
- MIME type support
- File size tracking
- Retention period management

## Architecture

### Models

#### Artifact Model

```python
class Artifact(ArtifactBase):
    id: str
    session_id: str
    user_id: str
    message_id: str
    artifact_type: ArtifactType
    source: ArtifactSource  # USER_UPLOAD or AI_GENERATED
    title: str
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]
    consent_required: bool
    consent_granted: Optional[bool]
    status: ArtifactStatus
    content: Optional[Dict[str, Any]]
    file_path: Optional[str]
    file_size: Optional[int]
    mime_type: Optional[str]
    original_filename: Optional[str]
    storage_uri: Optional[str]
    retention_expires_at: Optional[datetime]
```

#### Artifact Types

```python
class ArtifactType(str, Enum):
    # AI Generated
    CHART = "chart"
    REPORT = "report"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    VISUALIZATION = "visualization"
    DATA_EXPORT = "data_export"

    # User Uploaded
    PDF = "pdf"
    CSV = "csv"
    IMAGE = "image"
    DOCUMENT = "document"
    SPREADSHEET = "spreadsheet"
    OTHER = "other"
```

#### Artifact Sources

```python
class ArtifactSource(str, Enum):
    USER_UPLOAD = "user_upload"
    AI_GENERATED = "ai_generated"
```

#### Artifact Status

```python
class ArtifactStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CONSENT_REQUIRED = "consent_required"
    CONSENT_DENIED = "consent_denied"
```

## API Endpoints

### File Upload

```http
POST /{session_id}/artifacts/upload
Content-Type: multipart/form-data

file: <file>
message_id: <string>
title: <string> (optional)
description: <string> (optional)
```

### Consent Management

```http
POST /{session_id}/artifacts/{artifact_id}/consent
Content-Type: application/json

{
  "artifact_id": "string",
  "grant_consent": true
}
```

### Get Artifacts by Source

```http
GET /{session_id}/artifacts/source/{source}
```

### Get Artifacts Requiring Consent

```http
GET /{session_id}/artifacts/consent-required
```

## Usage Examples

### Creating User Upload Artifact

```python
# Upload a CSV file
artifact = await artifact_service.create_user_upload_artifact(
    session_id="session_123",
    user_id="user_456",
    message_id="msg_789",
    file_data=file_bytes,
    filename="financial_data.csv",
    mime_type="text/csv",
    title="Financial Data Upload",
    description="Monthly financial data"
)
```

### Creating AI-Generated Artifact

```python
# Create a chart artifact
artifact = await artifact_service.create_ai_generated_artifact(
    session_id="session_123",
    user_id="user_456",
    message_id="msg_789",
    artifact_type=ArtifactType.CHART,
    title="Portfolio Performance Chart",
    content={"data": [...], "config": {...}},
    description="Portfolio performance visualization"
)
```

### Granting Consent

```python
# Grant consent for an AI-generated artifact
artifact = await artifact_service.grant_consent_for_artifact(
    artifact_id="artifact_123",
    user_id="user_456"
)
```

### Denying Consent

```python
# Deny consent for an AI-generated artifact
artifact = await artifact_service.deny_consent_for_artifact(
    artifact_id="artifact_123",
    user_id="user_456"
)
```

## Integration with Runner Manager

The runner manager automatically creates AI-generated artifacts when the ADK runner produces them:

```python
# In RunnerManagerService.process_user_message()
async for event in response:
    if hasattr(event, "artifacts") and event.artifacts:
        for artifact_event in event.artifacts:
            artifact = await self.artifact_service_backend.create_ai_generated_artifact(
                session_id=backend_session_id,
                user_id=user_id,
                message_id=user_message["id"],
                artifact_type=self._map_adk_artifact_type(artifact_event.type),
                title=artifact_event.title or "Generated Artifact",
                content=artifact_event.content or {},
                description=artifact_event.description,
                metadata={
                    "adk_artifact_id": artifact_event.id,
                    "adk_session_id": session_id,
                    "source": "adk_runner",
                },
            )
```

## Consent Flow

### AI-Generated Artifacts

1. **Check User Consent**: System checks if user has global consent for storing artifacts
2. **If No Global Consent**: Artifact is created with `consent_required=True` and `status=CONSENT_REQUIRED`
3. **If Global Consent**: Artifact is created with `consent_required=False` and `status=COMPLETED`
4. **User Action**: User can grant/deny consent per artifact
5. **On Grant**: Artifact status becomes `COMPLETED`, content is preserved
6. **On Deny**: Artifact status becomes `CONSENT_DENIED`, content is removed

### User Uploads

1. **Implicit Consent**: User uploads have implicit consent (no additional consent needed)
2. **Direct Storage**: Artifacts are stored immediately with `status=COMPLETED`
3. **File Processing**: Files are saved to storage with unique names

## File Storage

### Current Implementation

- Files are stored locally in an `uploads/` directory
- Unique filenames are generated using UUID
- Original filenames are preserved in metadata

### Production Considerations

- Replace local storage with cloud storage (GCS, S3)
- Implement signed URLs for secure access
- Add file encryption for sensitive data
- Implement file lifecycle management

## Testing

Run the test script to verify the system:

```bash
cd backend
python test_artifact_system.py
```

The test script covers:

- AI-generated artifact creation with consent requirements
- User upload artifact creation
- Consent granting/denial
- Source-based filtering
- Session artifact retrieval

## Security Considerations

1. **File Validation**: Validate file types and sizes
2. **Access Control**: Ensure users can only access their own artifacts
3. **Consent Tracking**: Maintain audit trail of consent decisions
4. **Data Retention**: Respect user retention preferences
5. **File Security**: Secure file storage and access

## Future Enhancements

1. **Cloud Storage**: Migrate to cloud storage with signed URLs
2. **File Processing**: Add file processing capabilities (OCR, parsing)
3. **Versioning**: Support artifact versioning
4. **Sharing**: Enable artifact sharing between users
5. **Analytics**: Add usage analytics and insights
6. **Batch Operations**: Support batch consent operations
