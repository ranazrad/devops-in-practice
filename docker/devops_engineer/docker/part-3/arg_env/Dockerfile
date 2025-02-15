# Use a base image
FROM alpine:latest

# Define a build-time argument (not stored in the final image)
ARG APP_VERSION="1.0"

# Define an environment variable (stored in the final image)
ENV APP_NAME="MyApp"

# Print values during the build process
RUN echo "Building version: $APP_VERSION"

# Set an environment variable dynamically from the ARG
ENV APP_VERSION=$APP_VERSION

# Command that runs when the container starts
CMD echo "Running $APP_NAME version $APP_VERSION"
