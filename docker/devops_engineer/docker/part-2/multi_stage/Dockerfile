# === STAGE 1: BUILD ===
FROM python:3.9 AS build
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python -m compileall app
RUN echo "✅ BUILD FINISHED"


# === STAGE 2: LINT CHECK ===
FROM build AS lint
WORKDIR /app

RUN pip install --no-cache-dir pylint

ENV PYTHONPATH=/app

RUN echo "🔍 Running Pylint"
RUN pylint app --fail-under=6
RUN echo "✅ LINT FINISHED"


# === STAGE 3: UNIT TESTS ===
FROM lint AS test
WORKDIR /app

RUN pip install --no-cache-dir pytest pytest-cov

ENV PYTHONPATH=/app

RUN echo "🧪 Running Pytest"
RUN pytest app --junitxml=test-results.xml --cov=app --cov-report=xml --cov-report=term
RUN echo "✅ TESTS FINISHED"


# === STAGE 4: SONARQUBE ANALYSIS ===
FROM test AS sonar
WORKDIR /app

RUN apt-get update && apt-get install -y wget unzip && \
    wget -O /tmp/sonar-scanner.zip \
        https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip && \
    unzip /tmp/sonar-scanner.zip -d /opt/ && \
    ln -s /opt/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner

COPY sonar-project.properties /app/sonar-project.properties
RUN sonar-scanner
RUN echo "✅ SONAR FINISHED"


# === STAGE 5: FINAL IMAGE ===
FROM python:3.14.0a5-alpine3.20 AS runner
WORKDIR /app

# Copy from the *sonar* stage so that everything was done
COPY --from=sonar /app /app

CMD ["python", "app/main.py"]
