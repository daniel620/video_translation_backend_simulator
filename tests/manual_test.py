from client.client import TranslationClient

client = TranslationClient(base_url="http://127.0.0.1:8000")

# Create a job
job_id = client.create_job()
print(f"Created Job ID: {job_id}")

# Wait for completion
status = client.wait_for_completion(job_id, timeout=60)
print(f"Job Status: {status}")