# Fooocus CUDA Branch (cuda-rtx3060)

This branch provides a **CUDA‑only** build of Fooocus optimized for **RTX 30‑series GPUs**, particularly the RTX 3060.  The primary goal is to simplify the hardware backend logic and force the application to run exclusively on NVIDIA CUDA for maximum stability and performance.  The following changes have been implemented:

## Key Changes

- **Force CUDA execution:** All alternative backends such as DirectML, Intel XPU and Apple MPS have been disabled.  The `get_torch_device()` function in `ldm_patched/modules/model_management.py` now returns `torch.device("cuda")` directly.  If CUDA is not available, the application exits with a clear error message.

- **Low VRAM logic:** Low‑VRAM mode is only enabled automatically on GPUs with **4 GB or less** of VRAM.  GPUs with more memory will run in normal mode by default.  Use the `--always-normal-vram` command‑line option to force normal mode regardless of VRAM size.

- **Informative banner:** When the application starts, it prints the total VRAM and RAM detected and displays a clear banner indicating that it is running with the CUDA‑only configuration (e.g. “Running with RTX 3060 + CUDA”).

- **PyTorch nightly installation:** `entry_with_update.py` installs the latest **PyTorch nightly** builds (`torch` and `torchvision`) with CUDA 12.1 support using:

  ```bash
  python -m pip install --upgrade --pre --no-cache-dir torch torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cu121
  ```

  This command is executed automatically when running `entry_with_update.py`.  It ensures that you are using a CUDA‑compatible PyTorch version that takes advantage of the latest improvements.  If the installation fails, the script prints a warning and continues launching Fooocus.

- **Removal of alternative backend detections:** Code related to DirectML, Intel XPU (ipex) and MPS has been removed or disabled.  All device selection logic now funnels through CUDA.

## Usage

To run Fooocus with this branch:

1. **Switch to the branch:**

   ```bash
   git checkout cuda-rtx3060
   ```

2. **Run the application:**

   On Windows with the standalone build, the generated `run.bat` will call `entry_with_update.py`.  On other systems, you can execute `python entry_with_update.py` directly:

   ```bash
   python entry_with_update.py
   ```

3. **Verify CUDA usage:** On launch, you should see a banner similar to:

   ```
   Total VRAM 12288 MB, total RAM 16384 MB
   [Fooocus] Running with RTX 3060 + CUDA (cuda-rtx3060 branch)
   ```

   This indicates that the application detected your CUDA device and is configured accordingly.

## Notes

- This branch is **not** compatible with non‑NVIDIA hardware or systems without CUDA.  If you need CPU, MPS or other backend support, use the default `main` branch.
- The nightly PyTorch builds may change frequently; if you encounter issues, you can uninstall and reinstall specific versions by editing the pip install command in `entry_with_update.py`.

Happy rendering!