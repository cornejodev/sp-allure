#!/bin/bash
# Clean up old reports
rm -rf allure-report
rm -rf allure-results
BROWSER=chrome HEADLESS=false poetry run pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
