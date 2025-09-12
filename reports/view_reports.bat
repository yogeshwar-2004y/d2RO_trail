@echo off
echo ========================================
echo    AVIATRAX Test Reports Viewer
echo ========================================
echo.
echo Available reports:
echo.
echo 1. Backend Test Results (HTML)
echo 2. Backend Coverage Report (HTML)  
echo 3. Backend JUnit XML
echo 4. Backend Coverage XML
echo 5. Open Reports Folder
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Opening Backend Test Results...
    start backend\pytest_report.html
) else if "%choice%"=="2" (
    echo Opening Backend Coverage Report...
    start backend\coverage\index.html
) else if "%choice%"=="3" (
    echo Opening JUnit XML in default editor...
    start backend\junit.xml
) else if "%choice%"=="4" (
    echo Opening Coverage XML in default editor...
    start backend\coverage.xml
) else if "%choice%"=="5" (
    echo Opening Reports Folder...
    start .
) else (
    echo Invalid choice. Please run the script again.
)

echo.
echo Done!
pause
