# 🚀 DevOps URL Shortener Portal & CI/CD Pipeline

This project implements a web portal architecture and a fully automated **CI/CD pipeline** for a pure Python application (0% JavaScript), built according to modern DevOps best practices and designed to run natively on Linux environments.

## 🛠️ Tech Stack & Infrastructure
* **Backend Framework:** FastAPI (Python 3.11+) – asynchronous architecture closely mirroring serverless concepts.
* **Frontend Interface:** Pure HTML5 + HTTP Forms (Zero JavaScript dependency).
* **Development OS:** Fedora Linux (utilizing native system packages and configuration).
* **Automation (CI/CD):** GitHub Actions.

## ⚙️ CI/CD Pipeline Architecture (GitHub Actions)
Every time a developer performs a `git push`, the automated workflow executes the following stages:
1. **Linting & Validation:** Code syntax validation using `flake8` to ensure compliance with Python standards.
2. **Automated Testing:** Execution of test suites via `pytest` to verify endpoint availability, HTML rendering, and proper 307 redirect responses.
3. **Artifact Generation (CD Ready):** Upon successful validation, the production-ready code is packaged into a deployment artifact.

## 🚀 How to Run Locally on Fedora Linux

1. Install the required system packages:
   ```bash
   sudo dnf install -y python3-fastapi python3-uvicorn python3-multipart python3-pytest
   ```

2. Clone the repository and navigate to the project root:
   ```bash
   cd devops-url-shortener
   ```

3. Launch the development server:
   ```bash
   python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

4. Open your browser and navigate to:
   * Main Web Interface: `http://127.0.0`
   * Interactive API Docs: `http://127.0.0docs`

## 🧪 Running Tests
To validate the application behavior locally, execute:
```bash
python3 -m pytest
```
