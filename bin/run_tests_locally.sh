#!/bin/bash
poetry run pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
# allure open allure-report
