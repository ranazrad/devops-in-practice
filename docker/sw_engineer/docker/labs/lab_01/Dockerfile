# 1. Base Image - .NET SDK
FROM mcr.microsoft.com/dotnet/sdk:8.0

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy all files from host to container
COPY . .

# 4. Restore dependencies
RUN dotnet restore

# 5. Build the application to the 'out' folder
# Important: This creates 'acmeapi.dll' because the project name is 'acmeapi'
RUN dotnet build -c Release -o out

# 6. Entry Point
# This command runs the application when the container starts
ENTRYPOINT ["dotnet", "out/acmeapi.dll"]