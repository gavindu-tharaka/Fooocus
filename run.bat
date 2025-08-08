@echo off
REM run.bat for the cuda-rtx3060 branch
REM This script installs the PyTorch nightly build with CUDA 12.1 support
REM and then launches Fooocus.  It assumes you are running from the root
REM directory of the project and have a Python interpreter available.

echo [Setup] Installing PyTorch nightly with CUDA 12.1...
python.exe -m pip install --upgrade --pre --no-cache-dir torch torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cu121
if %ERRORLEVEL% neq 0 (
  echo [Setup] Failed to install PyTorch nightly.  Continuing with existing installation.
)

echo [Launch] Starting Fooocus with CUDA optimization...
python.exe Fooocus\entry_with_update.py %*
if %ERRORLEVEL% neq 0 (
  echo [Launch] Fooocus exited with an error.
)