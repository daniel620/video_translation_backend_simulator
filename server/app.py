from fastapi import FastAPI, HTTPException
import time
import random
from enum import Enum
import uuid
from typing import Dict
import logging
from config import MIN_DELAY, MAX_DELAY  # 引入配置文件中的参数

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ERROR = "error"

class JobTracker:
    def __init__(self, job_id: str, completion_time: float):
        self.job_id = job_id
        self.start_time = time.time()
        self.completion_time = completion_time
        self.status = JobStatus.PENDING

class TranslationServer:
    def __init__(self, min_delay: int = MIN_DELAY, max_delay: int = MAX_DELAY):
        self.jobs: Dict[str, JobTracker] = {}
        self.min_delay = min_delay
        self.max_delay = max_delay
    
    def create_job(self) -> str:
        """Create a new translation job with random completion time"""
        job_id = str(uuid.uuid4())
        completion_time = random.uniform(self.min_delay, self.max_delay)
        logger.info(f"Created job {job_id} with completion time {completion_time:.2f} seconds.")
        self.jobs[job_id] = JobTracker(job_id, completion_time)
        return job_id
    
    def get_job_status(self, job_id: str) -> JobStatus:
        """Get current status of a job"""
        if job_id not in self.jobs:
            logger.warning(f"Job {job_id} not found.")
            raise HTTPException(status_code=404, detail="Job not found")
            
        job = self.jobs[job_id]
        elapsed_time = time.time() - job.start_time
        
        # Simulate random errors (5% chance)
        if random.random() < 0.05:
            logger.error(f"Job {job_id} encountered an error.")
            job.status = JobStatus.ERROR
            return job.status
            
        # Check if job is completed
        if elapsed_time >= job.completion_time:
            logger.info(f"Job {job_id} completed.")
            job.status = JobStatus.COMPLETED
            
        return job.status

app = FastAPI()
server = TranslationServer()  # 使用配置文件中的延迟范围

@app.post("/jobs")
async def create_job():
    job_id = server.create_job()
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    status = server.get_job_status(job_id)
    return {"result": status}