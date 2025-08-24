@echo off
echo 🚀 Building WAN 2.2 Video Generation Docker Image
echo.
echo This may take 10-15 minutes for the first build...
echo.

docker build -t wan2-video-generation .

if %errorlevel% equ 0 (
    echo.
    echo ✅ Docker image built successfully!
    echo.
    echo 📋 Next steps:
    echo 1. Push to Docker Hub: docker tag wan2-video-generation YOUR_USERNAME/wan2-video-generation:latest
    echo 2. docker push YOUR_USERNAME/wan2-video-generation:latest
    echo 3. Create RunPod template using this image
    echo.
    pause
) else (
    echo.
    echo ❌ Docker build failed!
    echo Check the error messages above
    echo.
    pause
)