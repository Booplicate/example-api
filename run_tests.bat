@echo off

@echo Enabling venv...
@echo.

call "./venv/Scripts/activate"

@echo Running unit tests...
@echo.

python -m unittest discover -v tests --pattern "test_*.py"

@echo.
@echo Disabling venv...
@echo.

call "deactivate"

pause
