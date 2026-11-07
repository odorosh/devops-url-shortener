# DevOps Production URL Shortener 🚀

A robust, cloud-ready web application for URL shortening, built with industry-standard DevOps infrastructure and development practices. This project demonstrates the integration of a modern Python web framework with a reliable relational database storage layer, coupled with automated testing in a containerized cloud environment.

## 🛠️ Tech Stack
- **Backend:** Python 3.11, FastAPI
- **Database ORM:** SQLAlchemy (Enterprise-grade transactions, Connection Pooling)
- **Database:** PostgreSQL (Native Unix-domain socket execution for local environments)
- **Testing Suite:** Pytest, HTTPX
- **CI/CD Automation:** GitHub Actions (Automated linting, dynamic isolated PostgreSQL 15 service container orchestration)

## 🏗️ Infrastructure & Environment Architecture
The application is designed using a **Cloud-Agnostic** paradigm. Database connection configurations are handled dynamically using system environment variables:
1. **Local Development Environment (Fedora Linux):** The app connects via ultra-fast local Linux Unix-domain sockets using the dedicated privileges assigned to the `portal_user` database role.
2. **Testing & Validation Layer (GitHub Actions):** The automated pipeline spins up an isolated Docker service container running PostgreSQL 15, streams network parameters via `env` scopes, and runs integration test cases before compiling the release package.

## 🚀 Local Deployment Setup on Fedora
1. Ensure the native PostgreSQL service layer is active:
   ```bash
   sudo systemctl start postgresql
   ```
2. Install the production-grade dependency constraints:
   ```bash
   pip install -r requirements.txt
   ```
3. Boot the local Uvicorn development server:
   ```bash
   python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```
4. Access the production portal dashboard: `http://127.0.0`

## 🏁 CI/CD Pipeline Workflow
Every single `git push` or pull request targeting the `main` branch triggers an end-to-end automated verification cycle:
- **Code Quality Guard (Linting):** Python code style verification via strict `flake8` diagnostics.
- **Integration Layer Verification (Testing):** Automatic schema orchestration and live endpoint validation against a dynamic cloud database instance via `pytest`.
- **Artifact Delivery (CD Preview):** Packaging the verified source tree into a clean deployment artifact (`production-portal-code`).
