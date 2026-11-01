# Sample Application

A containerized FastAPI application built to demonstrate an end-to-end AWS DevOps and GitOps deployment workflow.

The application is deployed to Amazon EKS using Docker, Amazon ECR, Helm and Argo CD.

## Technology Stack

### Application
- Python 3.12
- FastAPI
- Pytest
- Prometheus Python Client

### Containerization and Security
- Docker
- Trivy

### CI/CD
- GitHub
- GitHub Actions
- AWS IAM OIDC
- Amazon ECR

### Deployment and Monitoring
- Kubernetes
- Amazon EKS
- Helm
- Argo CD
- Prometheus
- Grafana

## Application Endpoints

| Endpoint | Description |
|---|---|
| `/` | Returns application name and version |
| `/health` | Application health check |
| `/metrics` | Exposes Prometheus metrics |

Example health response:

```json
{
  "status": "ok"
}
```

## Run Locally

### Prerequisites

- Python 3.12
- pip

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the application:

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```

Access the endpoints:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/metrics

## Run Automated Tests

Run the test suite using Pytest:

```powershell
pytest -v
```

## Docker

Build the Docker image:

```powershell
docker build -t devops-demo-api:local .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 devops-demo-api:local
```

The application will be available at:

`http://localhost:8000`

## CI/CD Pipeline

The GitHub Actions workflow is located at:

`.github/workflows/ci.yml`

It runs on pushes and pull requests targeting the `main` branch.

### Pipeline Stages

1. **Checkout:** Retrieves the application source code.
2. **Python setup:** Configures Python 3.12.
3. **Dependency installation:** Installs application requirements.
4. **Testing:** Runs automated tests using Pytest.
5. **Docker build:** Builds an image tagged with the Git commit SHA.
6. **Security scanning:** Scans the image using Trivy for HIGH and CRITICAL vulnerabilities.
7. **AWS authentication:** Uses GitHub Actions OIDC to assume an IAM role.
8. **ECR login:** Authenticates Docker to Amazon ECR.
9. **Image push:** Pushes the commit-tagged image to ECR.
10. **GitOps update:** Updates the image tag in the separate GitOps repository.
11. **GitOps commit:** Commits and pushes the updated Helm values file.

The AWS authentication, image push and GitOps update stages run on pushes to `main`, not on pull requests.

### Trivy Configuration

Trivy scans the Docker image for operating-system and application-library vulnerabilities.

The current workflow uses `exit-code: 0`. This means vulnerability findings are reported but do not fail the pipeline. The scan is currently informational rather than a blocking security gate.

## AWS Authentication with OIDC

GitHub Actions authenticates to AWS using OpenID Connect.

This avoids storing long-lived AWS access keys in GitHub repository secrets.

An IAM role trust policy restricts which GitHub repository and branch can assume the role.

## GitOps Deployment

The application is deployed through a separate repository:

`Akshata-07/platform-gitops`

The deployment flow is:

```text
Application source code
        |
        v
GitHub Actions
        |
        v
Automated tests
        |
        v
Docker image build
        |
        v
Trivy security scan
        |
        v
GitHub OIDC authentication
        |
        v
Amazon ECR image push
        |
        v
GitOps image tag update
        |
        v
Argo CD synchronization
        |
        v
Helm deployment on Amazon EKS
```

The image tag uses the Git commit SHA to provide traceability between source code and the deployed container image.

## Repository Structure

```text
sample-application/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_app.py
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```

## Deployment Validation

The application deployment was validated through the complete CI/CD workflow:

- Automated tests passed.
- Docker image was built and scanned.
- Image was pushed to Amazon ECR.
- GitOps repository was updated automatically.
- Argo CD reported the application as Synced and Healthy.
- Two application replicas were running in EKS.
- The external application endpoint and health endpoint returned successful responses.

## Related Repositories

- Application: `Akshata-07/sample-application`
- Infrastructure: `Akshata-07/platform-infrastructure`
- GitOps: `Akshata-07/platform-gitops`