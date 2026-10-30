# Install MuMax3

Read this only when setting up MuMax3 or diagnosing a missing executable/GPU. Installing this agent skill does not install the simulator. This skill targets MuMax3 `.mx3` scripts; MuMax+ is a separate simulator with different installation and APIs, not a drop-in replacement.

## Check the environment first

Identify the OS, architecture, existing MuMax3 path, GPU and driver. Use read-only checks before choosing a download:

```text
nvidia-smi
nvidia-smi --query-gpu=name,driver_version,compute_cap --format=csv
```

Locate MuMax3 with `Get-Command mumax3 -ErrorAction SilentlyContinue` in PowerShell or `command -v mumax3` on Linux. In WSL, check `wsl --status` and `wsl -l -v` from Windows, then check GPU access inside the selected distribution. Some WSL GPU queries are unavailable; use the GPU model and NVIDIA documentation if needed.

MuMax3 3.12 requires an NVIDIA GPU with compute capability 5.0 or later and a compatible NVIDIA driver. The chosen binary's CUDA version can impose a higher GPU requirement: match all three in the [official download selector](https://mumax.github.io/download.html). An AMD/Intel-only or Apple Silicon machine needs access to a compatible NVIDIA host to run these simulations. Python is optional for MuMax3 itself and used separately by this skill's helpers.

## Prefer an official binary

1. Choose the native Windows or Linux archive matching the target OS, driver and GPU on the official download page. On Windows, prefer the native package unless an existing workflow needs Linux/WSL.
2. Download and extract it into a user-owned directory. Keep an existing working version until the replacement has been verified. These binaries do not require installing the full CUDA Toolkit, Go or a compiler.
3. Run the executable by its full path first. Add its containing directory to the user `PATH` if desired, then open a new terminal and confirm that it resolves to the intended installation.
4. In a scratch directory, run the official installation check, `mumax3 -test` (or `./mumax3 -test` on Linux before setting `PATH`). Record the exit code and reported version/GPU. This checks execution, not a scientific model. Use `mumax3 -vet path/to/script.mx3` for a subsequent script syntax check.

If startup fails, compare the driver and GPU against the selected binary before changing the system. Prefer another compatible official build when appropriate; do not assume the newest CUDA build supports every GPU. The CUDA version shown by `nvidia-smi` describes driver capability, not an installed Toolkit.

## WSL 2, when needed

Use a supported Windows host, WSL 2 with an updated kernel, a Linux distribution such as Ubuntu, and a compatible NVIDIA Windows driver. Follow [Microsoft's CUDA on WSL setup](https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl) and [NVIDIA's WSL guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html), then install the Linux MuMax3 binary inside WSL.

The Windows driver supplies GPU access to WSL: **do not install a Linux NVIDIA display driver inside WSL**. NVIDIA's WSL GPU requirements differ from native MuMax3's minimum; confirm support for the actual GPU. Only add a WSL-compatible CUDA Toolkit if compiling from source, avoiding packages that also install Linux drivers.

## Build from source only when necessary

Use the [official MuMax3 build instructions](https://github.com/mumax/3#building-from-source) for a required patch or unsupported binary combination. Select a release/tag and follow its requirements: NVIDIA driver, supported CUDA Toolkit, Go and compatible C toolchain. The current instructions specify CUDA at most 12.9; recheck for the selected source version rather than blindly installing the newest Toolkit. Linux uses GCC/make; Windows has additional MSVC and Go C-toolchain requirements and a `deploy_windows.ps1` build route. Set GPU architecture and toolchain paths as instructed, then verify the resulting executable.

## Agent-assisted installation

An agent can inspect the environment, select a compatible official package, explain the destination and proposed changes, and perform the installation when the user has authorized that scope. Reading this guide or asking for a script does not authorize software installation. Confirm any unapproved driver/Toolkit installation, administrator action, persistent environment change or reboot; continue within existing authorization without asking twice. Report the executable path, version, verification result and any remaining limitation.

Example request: “Check my OS and NVIDIA GPU, propose a compatible MuMax3 installation, then install it in a user directory once the required changes are authorized.”
