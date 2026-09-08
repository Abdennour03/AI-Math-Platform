# EduInsight AI

EduInsight AI is a FastAPI backend for student, teacher, course, exercise, submission, grading, and notification workflows.

## Run

Install dependencies and start the API:

```bash
python -m pip install -r requirements.txt
uvicorn app:app --reload
```

The interactive API is available at `http://127.0.0.1:8000/docs`.

## Architecture

```text
API route -> Controller -> Service -> Repository -> Database -> SQLite
```

Routes handle HTTP and Pydantic schemas. Controllers delegate to services. Services contain validation, authentication, authorization, relationship, and workflow rules. Repositories contain SQL persistence only. `database/database.py` owns the raw `sqlite3` connection and idempotent schema creation.

The project uses raw SQLite, not an ORM. The existing `eduinsight.db` file is preserved.

## Tests

```bash
python -m pytest -q
```

Focused tests cover database initialization, controller delegation, and grade creation, duplicate prevention, teacher ownership, and updates. See [ARCHITECTURE.md](ARCHITECTURE.md) for the complete refactor record.
