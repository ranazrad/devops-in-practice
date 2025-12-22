# Base image
FROM mcr.microsoft.com/dotnet/sdk:8.0


# 1. Build Arguments
ARG BUILD_VERSION


# 2. Environment Variables
ENV APP_VERSION=$BUILD_VERSION
ENV APP_MODE=Production


# 3. Optimization: Install tools in one layer and clean up
RUN apt-get update && apt-get install -y \
   curl \
   procps \
   && rm -rf /var/lib/apt/lists/*


WORKDIR /app


# 4. Layer Caching for dependencies
COPY *.csproj ./
RUN dotnet restore


# 5. Copying files (Layering)
COPY . ./
# Specific file copy as requested
COPY info.txt ./metadata/


# 6. Build application
RUN dotnet publish -c Release -o out


# 7. Security: Creating a non-root user
RUN useradd -m labuser && chown -R labuser /app
USER labuser


# Set Port (Default for .NET 8 is 8080)
EXPOSE 8080


ENTRYPOINT ["dotnet", "out/lab_02.dll"]
