#!/usr/bin/env python3
"""
Test script for the enhanced artifact system
"""

import asyncio
import os
import tempfile
from datetime import datetime

from src.models.artifact import ArtifactSource, ArtifactStatus, ArtifactType
from src.models.user import User, UserConsents, UserProfile
from src.repositories.user_repository import UserRepository
from src.services.artifact_service import ArtifactService


async def test_artifact_system():
    """Test the enhanced artifact system"""
    print("🧪 Testing Enhanced Artifact System")
    print("=" * 50)

    # Initialize services
    artifact_service = ArtifactService()
    user_repository = UserRepository()

    # Create a test user
    test_user = User(
        uid="test_user_123",
        profile=UserProfile(
            name="Test User",
            email="test@example.com",
            country="IN",
            risk_profile="moderate",
        ),
        consents=UserConsents(
            store_financial_snippets=False,
            store_artifacts=False,  # User hasn't consented to store artifacts
            retention_days=30,
            granted_at=datetime.now(),
        ),
    )

    # Save test user
    await user_repository.create_user(test_user)
    print("✅ Test user created")

    # Test 1: Create AI-generated artifact (should require consent)
    print("\n📊 Test 1: AI-Generated Artifact (Consent Required)")
    print("-" * 40)

    ai_artifact = await artifact_service.create_ai_generated_artifact(
        session_id="test_session_1",
        user_id="test_user_123",
        message_id="test_message_1",
        artifact_type=ArtifactType.CHART,
        title="Test Chart",
        content={"data": [1, 2, 3, 4, 5], "labels": ["A", "B", "C", "D", "E"]},
        description="A test chart artifact",
    )

    print(f"✅ AI artifact created: {ai_artifact.id}")
    print(f"   Status: {ai_artifact.status}")
    print(f"   Consent required: {ai_artifact.consent_required}")
    print(f"   Consent granted: {ai_artifact.consent_granted}")
    print(f"   Source: {ai_artifact.source}")

    # Test 2: Grant consent for AI artifact
    print("\n✅ Test 2: Grant Consent for AI Artifact")
    print("-" * 40)

    updated_artifact = await artifact_service.grant_consent_for_artifact(
        ai_artifact.id, "test_user_123"
    )

    print(f"✅ Consent granted for artifact: {updated_artifact.id}")
    print(f"   Status: {updated_artifact.status}")
    print(f"   Consent granted: {updated_artifact.consent_granted}")

    # Test 3: Create user upload artifact
    print("\n📁 Test 3: User Upload Artifact")
    print("-" * 40)

    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,value\nJohn,100\nJane,200\nBob,150")
        temp_file_path = f.name

    try:
        with open(temp_file_path, "rb") as f:
            file_data = f.read()

        upload_artifact = await artifact_service.create_user_upload_artifact(
            session_id="test_session_1",
            user_id="test_user_123",
            message_id="test_message_2",
            file_data=file_data,
            filename="test_data.csv",
            mime_type="text/csv",
            title="Test CSV Upload",
            description="A test CSV file upload",
        )

        print(f"✅ Upload artifact created: {upload_artifact.id}")
        print(f"   Status: {upload_artifact.status}")
        print(f"   Consent required: {upload_artifact.consent_required}")
        print(f"   Consent granted: {upload_artifact.consent_granted}")
        print(f"   Source: {upload_artifact.source}")
        print(f"   File size: {upload_artifact.file_size} bytes")
        print(f"   MIME type: {upload_artifact.mime_type}")

    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)

    # Test 4: Get artifacts by source
    print("\n🔍 Test 4: Get Artifacts by Source")
    print("-" * 40)

    ai_artifacts = await artifact_service.get_artifacts_by_source(
        "test_session_1", "test_user_123", ArtifactSource.AI_GENERATED
    )
    print(f"✅ AI-generated artifacts: {len(ai_artifacts)}")

    upload_artifacts = await artifact_service.get_artifacts_by_source(
        "test_session_1", "test_user_123", ArtifactSource.USER_UPLOAD
    )
    print(f"✅ User upload artifacts: {len(upload_artifacts)}")

    # Test 5: Get artifacts requiring consent
    print("\n⚠️ Test 5: Get Artifacts Requiring Consent")
    print("-" * 40)

    consent_required = await artifact_service.get_artifacts_requiring_consent(
        "test_session_1", "test_user_123"
    )
    print(f"✅ Artifacts requiring consent: {len(consent_required)}")

    # Test 6: Create AI artifact with user who has consent
    print("\n📊 Test 6: AI Artifact with User Consent")
    print("-" * 40)

    # Update user to have consent
    await user_repository.update_user_consents(
        "test_user_123", {"store_artifacts": True}
    )

    ai_artifact_with_consent = await artifact_service.create_ai_generated_artifact(
        session_id="test_session_1",
        user_id="test_user_123",
        message_id="test_message_3",
        artifact_type=ArtifactType.REPORT,
        title="Test Report",
        content={"summary": "This is a test report", "details": "More details here"},
        description="A test report artifact",
    )

    print(f"✅ AI artifact with consent created: {ai_artifact_with_consent.id}")
    print(f"   Status: {ai_artifact_with_consent.status}")
    print(f"   Consent required: {ai_artifact_with_consent.consent_required}")
    print(f"   Consent granted: {ai_artifact_with_consent.consent_granted}")

    # Test 7: Get all session artifacts
    print("\n📋 Test 7: Get All Session Artifacts")
    print("-" * 40)

    all_artifacts = await artifact_service.get_session_artifacts(
        "test_session_1", "test_user_123"
    )
    print(f"✅ Total artifacts in session: {len(all_artifacts)}")

    for artifact in all_artifacts:
        print(f"   - {artifact.title} ({artifact.source}) - {artifact.status}")

    print("\n🎉 All tests completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_artifact_system())
