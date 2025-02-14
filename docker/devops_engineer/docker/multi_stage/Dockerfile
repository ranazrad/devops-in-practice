# === STAGE 1: BUILD ===
FROM python:3.9 AS build
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python -m compileall app


# === STAGE 2: LINT CHECK ===
FROM python:3.9 AS lint
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pylint

COPY . .
RUN pylint app --fail-under=7


# === STAGE 3: UNIT TESTS ===
FROM python:3.9 AS test
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest pytest-junit

COPY . .
RUN pytest --junitxml=test-results.xml


# === STAGE 4: SONARQUBE ANALYSIS ===
FROM python:3.9 AS sonar
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest-junit sonar-scanner-cli

COPY . .
COPY --from=test /app/test-results.xml /app/test-results.xml
COPY sonar-project.properties /app/sonar-project.properties

RUN sonar-scanner


# === STAGE 5: FINAL IMAGE ===
FROM python:3.9 AS runner
WORKDIR /app

COPY --from=build /app /app

CMD ["python", "app/main.py"]
