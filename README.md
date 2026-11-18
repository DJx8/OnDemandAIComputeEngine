# On-Demand AI Compute Engine

A lightweight AI translation application that routes translation requests from a FastAPI backend to a remote Hugging Face Space running **IndicTrans2**. It provides a simple web interface and a REST API, while the translation model runs on remote compute instead of requiring a powerful local machine.

<p align="center">
  <a href="https://huggingface.co/spaces/Deejay888/Ondemand-translation-engine">Live Demo</a> ·
  <a href="https://github.com/DJx8/OnDemandAIComputeEngine">Source Code</a>
</p>

## Live Demo

Try the deployed translation interface:

**[On-Demand Translation Engine – Hugging Face Space](https://huggingface.co/spaces/Deejay888/Ondemand-translation-engine)**

## Features

- **English ↔ Indian language translation**
- Supports Hindi, Malayalam, Tamil, Kannada, Telugu, and Bengali
- **Remote inference:** sends translation requests to a Hugging Face Space powered by IndicTrans2
- **FastAPI REST API** for programmatic access
- Simple responsive web interface
- Automatic provider registration through a provider registry
- Hardware information endpoint for CPU, memory, and CUDA GPU detection
- Request validation, rate limiting, timeout handling, and retry logic

## Supported Languages

| Direction | Languages |
|---|---|
| English → Indian language | Hindi, Malayalam, Tamil, Kannada, Telugu, Bengali |
| Indian language → English | Hindi, Malayalam, Tamil, Kannada, Telugu, Bengali |

## Architecture

```text
User / Web Interface / API Client
              |
              v
       FastAPI Backend
              |
              v
        Compute Manager
              |
              v
       Provider Registry
              |
              v
   Hugging Face Space Provider
              |
        Gradio Client API
              |
              v
 Hugging Face Space (IndicTrans2)
              |
              v
       Translation Result
```

The backend validates the request and sends it to the configured Hugging Face Space through the Gradio client. The model inference happens remotely; the backend does not load IndicTrans2 locally.

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** HTML, CSS, JavaScript
- **Remote inference:** Hugging Face Spaces, Gradio Client
- **Translation model:** AI4Bharat IndicTrans2
- **Validation:** Pydantic
- **Rate limiting:** SlowAPI
- **System information:** psutil, PyTorch

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/DJx8/OnDemandAIComputeEngine.git
cd OnDemandAIComputeEngine
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`:

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

**Linux / macOS**

```bash
cp .env.example .env
```

Configure the values:

```env
HF_SPACE_ID=Deejay888/Ondemand-translation-engine
HF_TOKEN=your_huggingface_token_here
```

- `HF_SPACE_ID` identifies the Hugging Face Space used for translation.
- `HF_TOKEN` is optional for a publicly accessible Space. Add a Hugging Face access token if authentication is required. Keep tokens private and never commit your `.env` file.

### 5. Start the API and web application

```bash
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

Interactive API documentation is available at **http://127.0.0.1:8000/docs**.

## REST API

### Execute a translation

**Endpoint:** `POST /compute/execute`

**Request body:**

```json
{
  "task": "translation",
  "parameters": {
    "direction": "English → Indian Language",
    "text": "Hello, how are you?",
    "language": "Malayalam"
  }
}
```

For the reverse direction, use `Indian Language → English` and provide the selected Indian language in `language`.

**Example using curl:**

```bash
curl -X POST "http://127.0.0.1:8000/compute/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "translation",
    "parameters": {
      "direction": "English → Indian Language",
      "text": "Hello, how are you?",
      "language": "Malayalam"
    }
  }'
```

**Successful response:**

```json
{
  "status": "success",
  "task": "translation",
  "provider": "huggingface_space",
  "result": "..."
}
```

The translated text is returned in the `result` field.

### Other endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Web application |
| GET | `/health` | Backend health check |
| GET | `/compute/status` | Provider readiness and detected hardware information |
| GET | `/compute/tasks` | List supported compute tasks |
| POST | `/compute/execute` | Execute a supported AI task |

## Request Limits and Error Handling

- Maximum input length: **5,000 characters**
- Translation endpoint rate limit: **5 requests per minute per client IP**
- Remote request timeout: **180 seconds**
- The Hugging Face provider retries eligible failed requests up to **4 attempts**, with increasing delays.
- A remote provider or GPU quota issue can prevent a translation from completing. Availability and compute quotas are controlled by the Hugging Face Space and its hardware allocation.

Common API responses:

| HTTP status | Meaning |
|---|---|
| 200 | Request completed |
| 400 | Invalid or unsupported task/request |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 502 | Remote translation provider unavailable or timed out |

## Project Structure

```text
OnDemandAIComputeEngine/
├── app/
│   ├── main.py                 # FastAPI application and API routes
│   ├── schemas.py              # Translation request validation
│   ├── compute_manager.py      # Coordinates task execution
│   ├── provider_registry.py    # Registers and selects providers
│   └── hardware_detector.py    # CPU, memory, and GPU information
├── providers/
│   ├── base.py                 # Base provider interface
│   └── huggingface_space.py    # Hugging Face Space integration
├── frontend/
│   ├── index.html              # Web interface
│   ├── style.css               # UI styling
│   └── script.js               # Frontend/API interaction
├── .env.example
├── .gitignore
└── requirements.txt
```

## Notes

- This repository contains the **API backend and web frontend**. The translation model is hosted separately in the linked Hugging Face Space.
- The backend's hardware endpoint reports the machine running the backend; it does not select or provision the remote Hugging Face GPU.
- Actual inference availability depends on the remote Space status and its available compute quota.
- Do not publish Hugging Face access tokens or other secrets.

## Acknowledgements

- [AI4Bharat](https://ai4bharat.org/) for the IndicTrans2 translation models.
- [Hugging Face](https://huggingface.co/) for Spaces and model hosting.
- [FastAPI](https://fastapi.tiangolo.com/) and [Gradio](https://www.gradio.app/) for the application and remote inference interface.

## Author

**Dhananjay A V**

- GitHub: [@DJx8](https://github.com/DJx8)
- Project: [OnDemandAIComputeEngine](https://github.com/DJx8/OnDemandAIComputeEngine)
