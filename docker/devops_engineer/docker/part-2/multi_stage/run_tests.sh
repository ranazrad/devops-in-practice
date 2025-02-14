#!/bin/bash
echo "Running Lint checks..."
pylint app

echo "Running Unit Tests..."
pytest --junitxml=test-results.xml

echo "Running SonarQube analysis..."
sonar-scanner
