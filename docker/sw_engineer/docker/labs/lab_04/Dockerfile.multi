# Stage 1: Base & Restore (Caching Layer)
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base
WORKDIR /app
COPY ["src/MyApi/MyApi.csproj", "src/MyApi/"]
COPY ["tests/MyApi.Tests/MyApi.Tests.csproj", "tests/MyApi.Tests/"]
RUN dotnet restore "src/MyApi/MyApi.csproj"

# Stage 2: Build & Unit Tests
# If tests fail, the Docker build FAILS here.
FROM base AS test
COPY . .
WORKDIR "/app/tests/MyApi.Tests"
RUN dotnet test --logger:trx

# Stage 3: Publish
FROM test AS publish
WORKDIR "/app/src/MyApi"
RUN dotnet publish "MyApi.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Stage 4: Security Scan (Vulnerability Check)
FROM aquasec/trivy:latest AS security-scan
COPY --from=publish /app/publish /target
RUN trivy fs --exit-code 1 --severity HIGH,CRITICAL /target

# Stage 5: Final Production Image (The Lean Machine)
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
USER $APP_UID
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyApi.dll"]