# 1. Force x86_64 architecture so Selenium Manager works
FROM --platform=linux/amd64 python:3.11-slim

# 2. Install system deps
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    chromium-driver \
    chromium \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/bin/poetry

# 4. Set workdir & copy project
WORKDIR /app
COPY . .

# 5. Install dependencies (skip project itself)
RUN poetry install --no-root

# 6. Install Allure CLI
RUN curl -LO https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip && \
    unzip allure-2.27.0.zip -d /opt/ && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    rm allure-2.27.0.zip

# 7. Default command: run tests and emit Allure results
CMD ["poetry", "run", "pytest", "--alluredir=allure-results"]
