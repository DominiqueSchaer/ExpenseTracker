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


https://fastapi-app.wittysand-ac101e81.westeurope.azurecontainerapps.io
https://fastapi-app.wittysand-ac101e81.westeurope.azurecontainerapps.io/docs


# --------------------------------------
# build of docker

# --- config variables (set once) ---
$ACR = "tinyappexptrack"                        # your ACR name (no domain)
$IMG = "mila-expense-tracker-api"               # repository name in ACR
$TAG = (Get-Date -Format "yyyyMMdd-HHmmss")     # unique version tag; or set manually

# --- 1) build fresh ---
docker build --pull --no-cache -t "${IMG}:dev" -t "${IMG}:latest" .

# --- 2) test locally ---
docker run --rm -p 8000:8000 --name mila-api ${IMG}:latest
# (Ctrl+C when you're done testing)

# --- 3) login to ACR (logs Docker into the registry) ---
az acr login --name ${ACR}

# --- 4) tag for ACR (both unique and 'latest') ---
docker tag ${IMG}:latest "$ACR.azurecr.io/${IMG}:${TAG}"
docker tag ${IMG}:latest "$ACR.azurecr.io/${IMG}:latest"

# --- 5) push to ACR ---
docker push "${ACR}.azurecr.io/${IMG}:${TAG}"
docker push "${ACR}.azurecr.io/${IMG}:latest"

# --- 6) update Container App to the new, versioned image ---
az containerapp update `
  --name expense-tracker-api `
  --resource-group TinyApps `
  --image "$ACR.azurecr.io/${IMG}:${TAG}"
