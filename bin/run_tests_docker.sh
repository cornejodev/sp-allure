#!/bin/bash

set -e  # Exit on error

IMAGE_NAME=selenium-allure
CONTAINER_NAME=temp-selenium-runner

rm -rf allure-report
rm -rf allure-results

# Step 1: Build Docker image
echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME .

# Step 2: Run container (do not auto-remove so we can copy files)
echo "🚀 Running tests in Docker container..."
docker run --name $CONTAINER_NAME $IMAGE_NAME || true  # Don't exit if tests fail

# Step 3: Copy allure-results from container to local machine
echo "📁 Copying Allure results to host..."
rm -rf allure-results
docker cp $CONTAINER_NAME:/app/allure-results ./allure-results

# Step 4: Remove container
docker rm $CONTAINER_NAME

# Step 5: Generate and open the report
echo "📊 Generating Allure report..."
allure generate allure-results -o allure-report --clean
echo "🌐 Opening Allure report in browser..."
allure open allure-report
