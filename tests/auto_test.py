import pytest
from client.client import TranslationClient
from server.app import app
# from fastapi.testclient import TestClient
import uvicorn
import threading
import time

HOST = "127.0.0.1"
PORT = 8000

def run_server():
    """Run the FastAPI server in a separate thread"""
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")

@pytest.fixture(scope="session")
def server_fixture():
    """Start server for testing"""
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(1)  # Wait for server to start
    yield


def test_create_and_wait(server_fixture):
    """Test the entire lifecycle of creating a job and waiting for completion."""
    # Use TestClient's base_url
    translation_client = TranslationClient(f"http://{HOST}:{PORT}")
    print(f"Using base URL: {translation_client.base_url}")
    
    # Step 1: Create a job
    job_id = translation_client.create_job()
    assert job_id is not None, "Job ID should not be None"
    
    # Step 2: Wait for job completion
    status = translation_client.wait_for_completion(job_id, timeout=60)
    assert status in ("completed", "error"), f"Unexpected job status: {status}"
