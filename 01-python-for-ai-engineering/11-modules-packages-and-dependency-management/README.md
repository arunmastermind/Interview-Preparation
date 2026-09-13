## What this topic covers

Modules and packages keep code organized and reusable. Dependency management makes an AI project reproducible across development, CI, and production.

## Example 1: Module

Suppose `text_utils.py` contains:

```python
def normalize(text: str) -> str:
    return " ".join(text.lower().split())
```

Use it from another file:

```python
from text_utils import normalize

print(normalize("  Hello   AI  "))
```

## Example 2: Package structure

```
ai_app/
    __init__.py
    retrieval/
        __init__.py
        search.py
    llm/
        __init__.py
        client.py
    main.py
```

Then:

```python
from retrieval.search import search
from llm.client import LLMClient
```

## Example 3: Protect executable code

```python
def main():
    print("starting service")

if __name__ == "__main__":
    main()
```

This prevents `main()` from running merely because another module imports the file.

## Example 4: Dependency pinning

```
Django==5.2.5
numpy==2.3.2
pydantic==2.11.7
```

Pinning or otherwise constraining versions helps avoid unexpected production differences.

## Interview focus

Understand import resolution, absolute vs relative imports, `__init__.py`, circular imports, package structure, `pyproject.toml`, dependency pinning, lock files, and reproducible builds.

## Interview Mastery — Questions & Detailed Answers

### Core Interview Questions

**Q1. Module vs package — what is the difference?**

**Answer:** A module is typically a Python file containing code. A package organizes multiple modules into a directory structure and can expose a larger logical API.

**Q2. Why should imports be organized carefully?**

**Answer:** Clean imports improve readability, prevent circular dependencies, and make architectural boundaries visible. AI projects can become import-heavy because they combine web frameworks, model SDKs, databases, vector stores, and ML libraries.

**Q3. What is a circular import?**

**Answer:** Module A imports B while B directly or indirectly imports A during initialization. It often indicates overly coupled module design. Refactoring shared abstractions into a lower-level module is usually better than relying on local imports as a permanent fix.

**Q4. What is the purpose of `__init__.py`?**

**Answer:** It can mark a directory as a regular Python package and can also define package-level exports or initialization behavior. Modern Python also supports namespace packages without it, but `__init__.py` remains common and useful.

**Q5. Absolute vs relative imports?**

**Answer:** Absolute imports identify the package path from the project's import root and are generally easier to understand in larger applications. Relative imports can be useful within tightly scoped packages.

### Dependency Management

**Q6. Why pin dependencies in production AI services?**

**Answer:** ML and AI dependency graphs are complex. Pinning or tightly constraining versions improves reproducibility and prevents an unrelated package upgrade from changing runtime behavior.

**Q7. Requirements file vs `pyproject.toml`?**

**Answer:** A requirements file is commonly used to describe an environment's installable dependencies. `pyproject.toml` is the modern standard project configuration file and can define project metadata, dependencies, build configuration, and tool settings.

**Q8. What is a lock file?**

**Answer:** A lock file records resolved dependency versions, often including transitive dependencies, so environments can be reproduced more consistently.

**Q9. Direct vs transitive dependency?**

**Answer:** A direct dependency is explicitly required by your project. A transitive dependency is installed because one of your direct dependencies requires it. Production debugging should distinguish the two because upgrading a transitive package may have unexpected compatibility effects.

**Q10. How should AI projects handle heavyweight ML dependencies?**

**Answer:** Separate optional functionality where practical, use environment-specific dependency groups, and avoid installing large frameworks into services that do not need them. This reduces image size, build time, attack surface, and dependency conflicts.

### AI Engineering Scenarios

**Q11. How would you structure a production AI service?**

**Answer:** Keep API, domain/service logic, infrastructure integrations, configuration, and tests separated. For example:

```
app/
  api/
  services/
  domain/
  infrastructure/
  config/
  tests/
```

The exact structure can vary, but dependencies should generally point toward stable abstractions rather than making domain logic depend directly on every vendor SDK.

**Q12. How would you isolate a vector database SDK?**

**Answer:** Define an internal repository/interface such as `VectorStore.search()` and keep vendor-specific request/response conversion in infrastructure code. This makes provider replacement and unit testing easier.

**Q13. How would you manage dev/test/prod dependencies?**

**Answer:** Keep production runtime dependencies separate from development tooling where possible. Test frameworks, linters, formatters, notebooks, and profiling tools should not unnecessarily become production runtime dependencies.

**Q14. What causes dependency conflicts in AI projects?**

**Answer:** Common causes include incompatible versions of numerical libraries, GPU/CPU-specific packages, ML frameworks, model-serving libraries, and transitive dependencies. Reproducible environments and deliberate version constraints reduce these problems.

### Coding / Interview Exercises

**Q15. Create a small package with a clean public API.**

```
text_processor/
    __init__.py
    normalizer.py
    tokenizer.py
```

`__init__.py` can expose only the intended public functions rather than forcing callers to depend on internal module paths.

**Q16. How would you fix a circular import?**

**Answer:** First identify the dependency cycle. Then move shared types or abstractions into a lower-level module, invert the dependency using dependency injection, or restructure responsibilities. A local import can sometimes break initialization timing, but it should not hide a poor architecture.

### Common Traps

- Installing every dependency globally.
- Unpinned production environments.
- Mixing unrelated infrastructure logic into domain modules.
- Hiding circular imports with arbitrary local imports.
- Depending directly on vendor SDK types throughout the entire codebase.
- Including development-only packages in production images.
- Ignoring transitive dependency changes.

### Rapid-Fire Revision

- **Module:** Python source unit.
- **Package:** Organized collection of modules.
- **Circular import:** Cyclic module dependency.
- **Direct dependency:** Explicit project dependency.
- **Transitive dependency:** Dependency of another dependency.
- **Lock file:** Resolved dependency snapshot.
- **`pyproject.toml`:** Modern Python project configuration.
- **AI best practice:** Isolate vendor SDKs behind stable internal interfaces.