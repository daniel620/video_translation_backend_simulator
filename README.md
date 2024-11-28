# **HeyGen Video Translation Backend Simulator**

This project simulates a backend server for video translation jobs and provides a client library for interacting with the server. The solution is designed to satisfy the requirements of creating, monitoring, and completing translation jobs efficiently, while demonstrating good engineering practices.

---

## **Task Requirements and How This Solution Satisfies Them**

### **1. Simulating a Video Translation Backend**
- **Requirement**: Write a server that implements a `GET /status` API to return job statuses (`pending`, `completed`, `error`) with configurable delays.
- **Solution**:
  - The server, implemented using FastAPI, provides the following endpoints:
    - `POST /jobs`: Creates a new job with a random completion time and a unique job ID.
    - `GET /status/{job_id}`: Returns the status of a given job (`pending`, `completed`, or `error`).
  - Job completion time is configurable using `MIN_DELAY` and `MAX_DELAY` in `config.py`.
  - Random errors are introduced (5% chance) to simulate real-world service instability.

### **2. Efficient Client Library**
- **Requirement**: Write a client library that interacts with the server, avoiding trivial polling while minimizing delays and resource usage.
- **Solution**:
  - The client library (`TranslationClient`) provides methods to:
    - `create_job()`: Create a new job by calling the server's `POST /jobs` endpoint.
    - `get_status(job_id)`: Check the status of a job using the server's `GET /status/{job_id}` endpoint.
    - `wait_for_completion(job_id, timeout)`: Efficiently poll for the job's status using **exponential backoff** to reduce server load.
  - The library handles errors (e.g., network failures or server issues) gracefully and provides options for retries, timeouts, and customizable polling intervals.

### **3. Customer Mindset**
- **Requirement**: Design the library with third-party usability in mind.
- **Solution**:
  - The client library is easy to use and customizable:
    - Allows users to configure polling intervals, timeouts, and backoff factors.
    - Provides clear methods for job creation and status monitoring.
  - Includes comprehensive error handling and logging to assist users in debugging.

### **4. Deliverables**
- **Public Git Repository**:
  - Includes all required components: server, client, tests, and documentation.
- **Integration Test**:
  - Demonstrates end-to-end interaction between the client and server.
- **Documentation**:
  - This `README.md` explains how to use the server, client, and test cases.

---

## **Features**

### **Server**
- Simulates a backend for video translation jobs with configurable delays and random errors.
- Provides two endpoints:
  - `POST /jobs`: Create a new job.
  - `GET /status/{job_id}`: Check the status of an existing job.
- Implements job tracking, status updates, and error simulation.

### **Client Library**
- Provides an easy-to-use Python library for interacting with the server.
- Uses efficient polling with exponential backoff to reduce server load.
- Handles errors, retries, and timeouts gracefully.

### **Tests**
- Includes manual and automated tests to demonstrate and validate functionality.

---

## **Setup**

### **1. Install Dependencies**
Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

### **2. Run the Server**
Start the server using the following command:
```bash
uvicorn server.app:app --reload --host 127.0.0.1 --port 8000
```

The server will run on `http://127.0.0.1:8000`.

---

## **Usage**

### **Client Library Example**
The client library (`TranslationClient`) allows you to interact with the server easily. Here’s an example:

```python
from client.client import TranslationClient

client = TranslationClient(base_url="http://127.0.0.1:8000")

# Step 1: Create a job
job_id = client.create_job()
print(f"Created Job ID: {job_id}")

# Step 2: Wait for job completion
status = client.wait_for_completion(job_id, timeout=60)
print(f"Job Status: {status}")
```

---

## **Testing**

This project includes two types of tests: manual tests for demonstrating client-server interaction and automated tests for validating functionality.

### **1. Manual Test**
The manual test (`tests/manual_test.py`) demonstrates the full lifecycle of interacting with the server using the client library.

#### **Run the Manual Test**
1. Start the server:
   ```bash
   uvicorn server.app:app --reload --host 127.0.0.1 --port 8000
   ```
2. Run the manual test script:
   ```bash
   python -m tests.manual_test
   ```

#### **Expected Output**
You will see output similar to the following:
```
Created Job ID: 123e4567-e89b-12d3-a456-426614174000
Job Status: completed
```

---

### **2. Automated Test**
The automated test (`tests/auto_test.py`) validates the integration between the server and client using `pytest`.

#### **Run the Automated Test**
Use the following command to run the test:
```bash
pytest tests/auto_test.py --log-cli-level=INFO -v
```

#### **Test Cases Covered**
- **Create Job**:
  - Validates that the server responds with a valid job ID.
- **Wait for Completion**:
  - Ensures the client can poll the server until the job completes or fails, respecting the timeout.

#### **Expected Output**
If all tests pass, the output will look like this:
```
tests/auto_test.py::test_create_and_wait INFO     Using base URL: http://127.0.0.1:8000
tests/auto_test.py::test_create_and_wait INFO     Created Job ID: abc123
tests/auto_test.py::test_create_and_wait INFO     Final Job Status: completed
PASSED
```

---

## **Configuration**

You can configure the server and client parameters by modifying the `config.py` file or using environment variables:

- **Server Configuration**:
  - `MIN_DELAY`: Minimum delay for job completion (default: `10` seconds).
  - `MAX_DELAY`: Maximum delay for job completion (default: `30` seconds).

- **Client Configuration**:
  - `INITIAL_INTERVAL`: Initial polling interval for the client (default: `1.0` seconds).
  - `MAX_INTERVAL`: Maximum polling interval (default: `30.0` seconds).
  - `BACKOFF_FACTOR`: Multiplier for exponential backoff (default: `1.5`).

---

## **Summary of Requirements Fulfillment**

| **Requirement**                         | **How This Solution Satisfies It**                                                                 |
|-----------------------------------------|----------------------------------------------------------------------------------------------------|
| Simulate a video translation backend     | The server provides endpoints for job creation and status checking with configurable delays.       |
| Efficient polling in client library     | The client uses exponential backoff to reduce polling frequency over time.                        |
| Demonstrate customer mindset            | The client library is user-friendly, flexible, and includes robust error handling and logging.    |
| Deliverables                            | Includes a public repository, integration tests, and comprehensive documentation.                 |

---