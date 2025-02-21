# Galgo-Full

# LangFlow & Environment Setup Guide

## Overview
This guide provides step-by-step instructions to:
- Set up the `.env` file for database and LangFlow configuration.
- Run LangFlow using Docker and Docker Compose following the official setup.
- Verify LangFlow is running and connected to the backend.
- Create a blank flow in LangFlow and import predefined flows from the repository.

---

## 1. Setting Up the `.env` File
Before running the project, create a `.env` file in the root directory and add the following:

```env
# MySQL Database Configuration
MYSQL_PASSWORD=your_password
MYSQL_HOST=18.223.196.217
MYSQL_USER=your_username
MYSQL_DATABASE=core_db
MYSQL_PORT=3306

# LangFlow API URL (Localhost by default)
LANGFLOW_URL=http://localhost:7860
```

---

## 2. Installing Prerequisites
### Step 1: Install Docker & Docker Compose
If you have not installed Docker yet, download and install it from:

- [Docker Installation Guide](https://www.docker.com/get-started)

After installation, verify Docker and Docker Compose by running:
```sh
docker --version
docker compose version
```

---

## 3. Cloning & Setting Up LangFlow
### Step 2: Clone LangFlow Repository
Clone the LangFlow repository from GitHub:

```sh
git clone https://github.com/langflow-ai/langflow.git
```

Navigate to the `docker_example` directory:
```sh
cd langflow/docker_example
```

---

## 4. Running LangFlow Using Docker Compose
### Step 3: Start LangFlow
Execute the following command inside the `docker_example` directory:

```sh
docker compose up
```

This command will:
- Pull the LangFlow image (if not already downloaded).
- Start the LangFlow service and make it available at `http://localhost:7860`.

Once it is running, open your browser and visit:
```
http://localhost:7860
```
If the UI loads, LangFlow is successfully running.

For more information on deploying LangFlow with Docker, refer to the official LangFlow Deployment Guide:  
[LangFlow Docker Deployment Docs](https://docs.langflow.org/Deployment/deployment-docker)

---

### 5. Creating a Blank Flow and Importing Predefined Flows

Once LangFlow is running, follow these steps to create a new blank flow and import existing flows from the repository:

1. **Open LangFlow**: Navigate to `http://localhost:7860` in your browser.
2. **Create a Blank Flow**:
   - Click on the **New Flow** button.
   - Name the flow appropriately.
   - Click **Create** to start a new flow.
3. **Import Predefined Flows**:
   - In the LangFlow UI, locate the **Import Flow** option.
   - Navigate to the `flows/` folder in the repository.
   - Select the desired `.json` file and upload it to LangFlow.
   - The flow will be loaded and ready for use.

---

### 6. Stop LangFlow (If Needed)
To stop LangFlow, run:
```sh
docker compose down
```
This will gracefully shut down the container.

---

### 7. Verify LangFlow is Running
Once LangFlow is running, confirm that the backend can communicate with it.

Run the following command inside your backend directory:
```sh
curl http://localhost:7860
```
If you receive an HTTP response, the connection is successful.

---

## 8. Next Steps
- Keep LangFlow running in the background while developing.
- Once set up, continue with backend and frontend integration.

---

## Helpful Links
- [LangFlow GitHub Repository](https://github.com/logspace-ai/langflow)
- [LangFlow Docker Deployment Guide](https://docs.langflow.org/Deployment/deployment-docker)
- [Docker Compose Guide](https://docs.docker.com/compose/)

