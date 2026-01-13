## Running the Project with Docker

This project is containerized using Docker and Docker Compose for easy setup and deployment. Below are the instructions and details specific to this project:

### Requirements & Versions
- **Python Version:** 3.11 (as specified in the Dockerfile: `python:3.11-slim`)
- **Dependencies:** All Python dependencies are installed from `requirements.txt` inside a virtual environment (`.venv`) during the build process.

### Environment Variables
- The project supports environment variables via a `.env` file. If you have a `.env` file, uncomment the `env_file: ./.env` line in the `docker-compose.yml` to enable it.

### Build and Run Instructions
1. **Build and start the service:**
   ```sh
   docker compose up --build
   ```
   This will build the Docker image and start the `python-app` service.

2. **Environment Variables:**
   - If your application requires environment variables, ensure you have a `.env` file in the project root. Uncomment the `env_file` line in `docker-compose.yml` if needed.

3. **Ports:**
   - No ports are exposed by default. If your app exposes an HTTP API (e.g., on port 8000), uncomment and adjust the `ports` section in `docker-compose.yml`:
     ```yaml
     ports:
       - "8000:8000"
     ```

### Special Configuration
- The application runs as a non-root user (`appuser`) for improved security.
- All application code is located in the `app/` directory and is copied into the container during build.
- No external services (databases, caches, etc.) are configured by default. If you add such services, update the `docker-compose.yml` accordingly.

### Default Command
- The container runs the application using:
  ```sh
  python -m app.main
  ```
  If your entrypoint changes, update the `CMD` in the Dockerfile as needed.

---

*For further customization, refer to the `Dockerfile` and `docker-compose.yml` in the project root.*
