@echo off
echo 🚀 Mario's WAN 2.2 Docker Push Script
echo.

REM Check if the image exists
docker images wan2-video-generation --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | findstr wan2-video-generation >nul
if %errorlevel% neq 0 (
    echo ❌ Docker image 'wan2-video-generation' not found!
    echo Make sure the build completed successfully first.
    pause
    exit /b 1
)

echo ✅ Found Docker image 'wan2-video-generation'
echo.

echo 🏷️ Tagging image for Docker Hub...
docker tag wan2-video-generation mariogx/wan2-video-generation:latest

echo 🔑 Please login to Docker Hub...
docker login

echo 📤 Pushing to Docker Hub (mariogx/wan2-video-generation:latest)...
docker push mariogx/wan2-video-generation:latest

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS! Image pushed to Docker Hub
    echo.
    echo 📋 Your image URL: mariogx/wan2-video-generation:latest
    echo.
    echo 🚀 Next steps:
    echo 1. Go to https://runpod.io/console/user/templates
    echo 2. Create new template with image: mariogx/wan2-video-generation:latest
    echo 3. Deploy serverless endpoint using A100 80GB GPU
    echo 4. Update your .env with the new endpoint URL
    echo.
    echo Your RunPod API Key: rpa_UBJUKYG839LGMV2F3TPYFBTYNLVYW7I5NMB0V7YT1gdzhd
    echo.
) else (
    echo.
    echo ❌ Push failed! Check the error above.
    echo Make sure you're logged into Docker Hub.
    echo.
)

pause