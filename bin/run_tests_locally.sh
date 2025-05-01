#!/bin/bash
# 1) Clean up old reports
rm -rf allure-report
rm -rf allure-results
poetry run pytest --headed --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
