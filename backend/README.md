# What is FastAPI?

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.  
It is designed for building RESTful APIs quickly and efficiently, with automatic data validation, interactive documentation, and high performance powered by Starlette and Pydantic.

**Key features:**
- Automatic OpenAPI and interactive docs (Swagger UI, ReDoc)
- Data validation and serialization using Python type hints and Pydantic
- Asynchronous support (async/await)
- High performance (comparable to Node.js and Go)
- Easy integration with modern Python tooling

**Official site:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

# How to install the Heroku CLI

If you see `'heroku' is not recognized as the name of a cmdlet...`, it means the Heroku CLI is not installed or not in your PATH.

## To install the Heroku CLI:

1. Go to [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. Download and install the Heroku CLI for your operating system.
3. After installation, restart your terminal or command prompt.
4. Run `heroku --version` to verify the installation.

Now you can use Heroku commands like `heroku create` and `heroku push`.

# How to install Docker

If you see `'docker' is not recognized as the name of a cmdlet...`, it means Docker is not installed or not in your PATH.

## To install Docker:

1. Go to [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Download and install Docker Desktop for your operating system (Windows, Mac, or Linux).
3. After installation, restart your terminal or command prompt.
4. Run `docker --version` to verify the installation.

Now you can use Docker commands like `docker build` and `docker run`.

# Running as a Container App on Azure

To deploy this FastAPI backend as a container app on Azure:

1. **Add a Dockerfile** to the backend directory (see project root or backend/).
2. **Build the Docker image:**
   ```bash
   docker build -t my-fastapi-app .
   ```
3. **Test locally (optional):**
   ```bash
   docker run -p 8000:8000 my-fastapi-app
   ```
4. **Push the image to a container registry** (e.g., Azure Container Registry or Docker Hub).
5. **Create an Azure Container App** and configure it to use your image.
6. **Set environment variables and networking as needed in Azure Portal.**

See [Azure Container Apps documentation](https://learn.microsoft.com/en-us/azure/container-apps/) for detailed steps.

# Testing the Docker Container Locally

To test your FastAPI backend container locally:

1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd path/to/Mila_Expense_Tracker/backend
   ```

2. Build the Docker image:
   ```bash
   docker build -t my-fastapi-app .
   ```

3. Run the container:
   ```bash
   docker run -p 8000:8000 my-fastapi-app
   ```

4. Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) to access the FastAPI interactive API docs.


Application URL:
https://fastapi-app.icywave-1777a797.westeurope.azurecontainerapps.io

http://localhost:8000/docs#/

az acr create --resource-group TinyApps --name tinyappexptrack --sku Basic


az acr login --name tinyappexptrack

docker tag my-fastapi-app tinyappexptrack.azurecr.io/my-fastapi-app:latest
docker push tinyappexptrack.azurecr.io/my-fastapi-app:latest

az containerapp env create --name tinyapps-env --resource-group TinyApps --location westeurope

az containerapp create `
  --name expense-tracker-api `
  --resource-group TinyApps `
  --environment tinyapps-env `
  --image tinyappexptrack.azurecr.io/my-fastapi-app:latest `
  --registry-server tinyappexptrack.azurecr.io `
  --target-port 8000 `
  --ingress external

https://fastapi-app.wittysand-ac101e81.westeurope.azurecontainerapps.io
https://fastapi-app.wittysand-ac101e81.westeurope.azurecontainerapps.io/docs



# -> to be done for new push to Azure
# --------------------------------------

# from your backend repo root
docker build -t my-fastapi-app:$(git rev-parse --short HEAD) .
# if you’re on Apple Silicon and your base image is amd64:
# docker build --platform linux/amd64 -t my-fastapi-app:$(git rev-parse --short HEAD) .

az acr login --name tinyappexptrack

TAG=$(git rev-parse --short HEAD)
docker tag my-fastapi-app:$TAG tinyappexptrack.azurecr.io/my-fastapi-app:$TAG
docker push tinyappexptrack.azurecr.io/my-fastapi-app:$TAG

az containerapp update \
  --name expense-tracker-api \
  --resource-group TinyApps \
  --image tinyappexptrack.azurecr.io/my-fastapi-app:$TAG
