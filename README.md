# BeautifulMind Streamlit app

A single self-contained Streamlit application that replaces the previous
microservice stack (Django backend, FastAPI ai/orchestrator/whatsapp services,
React frontend, Postgres). It keeps the same domain (doctors, patients, and
anonymized voice notes) with three role-based experiences.

## Roles

- Login routes each user to their role: doctor, patient, or admin.
- Doctor: add / edit / remove their own patients. Creating a patient
  generates a username and a one-time password shown once.
- Patient: must change the one-time password on first login, then can
  record a new voice note (transcribed via Whisper, anonymized via GPT and
  stored), review past notes as anonymized text, and change their password.
- Admin: add / edit doctors and patients, view usage statistics per
  patient and aggregated (# voice requests, voice duration, transcribed
  tokens), and manage application secrets.

## Configuration

Voice transcription needs OpenAI credentials. Sign in as an administrator and
add these under Application Secrets (or set them as environment variables):

- `OPENAI_API_KEY` (required)
- `OPENAI_CHAT_MODEL` (default `gpt-4o-mini`)
- `OPENAI_STT_MODEL` (default `whisper-1`)

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Or with Docker:

```bash
docker build -t beautifulmind-streamlit .
docker run -p 8501:8501 beautifulmind-streamlit
```

Data is stored in a local SQLite database at `data/beautifulmind.db`.
