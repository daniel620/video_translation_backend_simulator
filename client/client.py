import httpx
import time
from typing import Callable, Optional
import logging
from config import INITIAL_INTERVAL, MAX_INTERVAL, BACKOFF_FACTOR 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationClient:
    def __init__(self, base_url: str, initial_interval: float = INITIAL_INTERVAL,
                 max_interval: float = MAX_INTERVAL, backoff_factor: float = BACKOFF_FACTOR):
        """
        Initialize the translation client with exponential backoff settings.
        
        Args:
            base_url: Server base URL
            initial_interval: Starting polling interval in seconds
            max_interval: Maximum polling interval in seconds
            backoff_factor: Multiplier for exponential backoff
        """
        self.base_url = base_url.rstrip('/')
        self.initial_interval = initial_interval
        self.max_interval = max_interval
        self.backoff_factor = backoff_factor
    
    def create_job(self) -> str:
        """Create a new translation job"""
        with httpx.Client() as client:
            response = client.post(f"{self.base_url}/jobs")
            response.raise_for_status()
            return response.json()["job_id"]
    
    def get_status(self, job_id: str) -> str:
        """Get status for a specific job"""
        with httpx.Client() as client:
            response = client.get(f"{self.base_url}/status/{job_id}")
            response.raise_for_status()
            return response.json()["result"]
    
    def wait_for_completion(self, job_id: str, 
                          callback: Optional[Callable[[str], None]] = None,
                          timeout: Optional[float] = None) -> str:
        """
        Wait for job completion with exponential backoff.
        
        Args:
            job_id: Job ID to monitor
            callback: Optional callback function for status updates
            timeout: Optional timeout in seconds
            
        Returns:
            Final job status ("completed" or "error")
        """
        start_time = time.time()
        current_interval = self.initial_interval
        
        while True:
            status = self.get_status(job_id)
            logger.info(f"Job {job_id} status: {status}")
            
            if callback:
                callback(status)
            
            if status in ("completed", "error"):
                return status
                
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Job {job_id} timed out")
            
            # Exponential backoff with max limit
            time.sleep(current_interval)
            current_interval = min(
                current_interval * self.backoff_factor,
                self.max_interval
            )