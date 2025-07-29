@echo off
echo Running OTP Integration Tests...
echo ================================

REM Use the Python from the virtual environment
call .venv\Scripts\activate
python run_integration_test.py

echo.
echo Tests completed!
pause