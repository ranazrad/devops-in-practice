# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /source
COPY src/*.csproj .
RUN dotnet restore
COPY src/ .
RUN dotnet publish -c Release -o /app

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app .

# Create the logs directory and set permissions
RUN mkdir -p /app/logs

EXPOSE 8080
ENTRYPOINT ["dotnet", "LogApp.dll"]