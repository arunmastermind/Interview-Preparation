## What this topic covers

Virtual environments isolate project dependencies so one Python project cannot accidentally break another. This is essential when AI projects require different versions of Python, PyTorch, NumPy, CUDA-related packages, or web frameworks.

## Example 1: Create and activate

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

## Example 2: Install and freeze dependencies

```bash
python -m pip install requests numpy
python -m pip freeze > requirements.txt
```

Recreate the environment:

```bash
python -m pip install -r requirements.txt
```

## Example 3: Verify the interpreter

```bash
which python
python --version
python -m pip --version
```

Using `python -m pip` reduces the chance of installing packages into a different interpreter's environment.

## Example 4: Project setup pattern

```
my-ai-service/
    .venv/
    src/
    tests/
    pyproject.toml
    README.md
```

The environment itself should normally be excluded from Git.

## Interview focus

Explain why virtual environments exist, how dependency isolation works, how you reproduce an environment in CI/production, and the difference between environment isolation and container isolation.

## Interview Mastery — Questions & Detailed Answers

### Core Interview Questions

**Q1. Why use virtual environments?**

**Answer:** A virtual environment isolates project dependencies from the system Python and other projects. This prevents incompatible package versions from interfering with each other.

**Q2. `venv` vs system Python?**

**Answer:** System Python is shared at the machine level; a virtual environment provides a project-specific interpreter and site-packages directory.

**Q3. Why does environment reproducibility matter for AI engineering?**

**Answer:** AI systems depend on many tightly coupled libraries. Reproducing the same Python version and dependency versions is important when moving between local development, CI, containers, and production.

**Q4. What is the difference between activating a virtual environment and using its interpreter directly?**

**Answer:** Activation changes shell environment variables such as `PATH`. You can also call the environment's Python executable directly without activating it.

**Q5. How do you verify which Python environment is active?**

```bash
which python
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Using `python -m pip` helps ensure pip corresponds to the Python interpreter you are using.

### AI Engineering Scenarios

**Q6. A package works locally but fails in CI. What do you check?**

**Answer:** Compare Python versions, OS/platform, architecture, dependency versions, environment variables, optional dependencies, system libraries, and lock/requirements files. Do not assume that a successful local install proves the environment is reproducible.

**Q7. Why should you avoid `pip install` blindly in production?**

**Answer:** It can resolve newer versions than the environment was tested with and introduce compatibility or security issues. Production builds should use controlled dependency specifications and preferably a reproducible lock/resolution process.

**Q8. How do virtual environments interact with Docker?**

**Answer:** Docker already provides process/filesystem isolation, so a separate Python virtual environment inside a container is often unnecessary. The decision depends on the image/build strategy, but duplicating isolation can add complexity without much benefit.

**Q9. How would you reproduce an environment for an interview coding task?**

**Answer:** Record the Python version, create a fresh virtual environment, install the specified dependencies, and run tests from the clean environment rather than relying on globally installed packages.

### Coding / Practical Questions

**Q10. Create and use a virtual environment.**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activation uses the corresponding `.venv\Scripts\Activate.ps1` path.

**Q11. How would you detect accidental global installation?**

```bash
python -c "import sys; print(sys.prefix); print(sys.base_prefix)"
```

When the environment is active, these values normally differ.

**Q12. What should be excluded from version control?**

**Answer:** The virtual environment directory itself, caches, secrets, generated artifacts, and machine-specific files. Store dependency specifications rather than the environment directory.

### Common Traps

- Using global `pip` with a different Python interpreter.
- Forgetting to record dependency versions.
- Committing `.venv/` to Git.
- Assuming a virtual environment solves OS-level dependency problems.
- Reproducing only direct dependencies while ignoring transitive dependencies.

### Rapid-Fire Revision

- **Virtual environment:** Isolated Python runtime/dependencies.
- **`venv`:** Standard-library environment creation tool.
- **`python -m pip`:** Ensures pip is associated with that Python interpreter.
- **Reproducibility:** Same interpreter + controlled dependencies + consistent environment assumptions.
- **Docker:** Often provides enough isolation that an internal venv is optional.