# Module 15 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 15](README.md) · [Quiz](QUIZ.md)

---

### 1. Are type hints enforced at runtime?

**Say:** No. The interpreter stores them in `__annotations__` and ignores them. Static checkers (mypy, pyright) and IDEs use them. Some libraries **do** read them at runtime to validate data, notably Pydantic and FastAPI.

---

### 2. Why use type hints in a dynamic language?

**Say:** They catch whole classes of bugs before runtime (None handling, wrong argument types), make refactoring safe, give better autocomplete, and serve as always-up-to-date documentation. On a team, they make large codebases manageable.

---

### 3. `Optional[X]` vs `X | None`?

**Say:** They're the same: "X or None". `X | None` is the modern syntax (3.10+). `Optional` doesn't mean "optional argument"; a default value does that.

---

### 4. `Any` vs `object`?

**Say:** `Any` **turns off** checking: everything is allowed. `object` accepts any value but lets you do almost nothing with it until you narrow it (`isinstance`). Prefer `object` or a precise type; `Any` should be rare.

---

### 5. What is a `TypeVar` / generic?

**Say:** A placeholder type that links inputs and outputs: `def first(xs: list[T]) -> T`. Passing `list[int]` gives `int` back. `Generic[T]` makes classes like `Page[T]` or `Repository[T]` type-safe. Python 3.12 has the shorter syntax `def first[T](xs: list[T]) -> T`.

---

### 6. `Protocol` vs `ABC`?

**Say:** A Protocol is **structural** typing: any class with the right methods matches, with no inheritance. An ABC is **nominal**: you must subclass it. Protocols are great for dependencies you want to fake in tests.

---

### 7. When do you use `TypedDict` vs a dataclass vs a Pydantic model?

**Say:**
- **`TypedDict`**: describes plain dicts, such as JSON you pass around unchanged.
- **dataclass**: internal objects with behaviour, no validation.
- **Pydantic**: data from **outside** (API bodies, config, env vars) that must be validated and converted.

---

### 8. What does mypy's `--strict` do?

**Say:** It turns on all the optional checks: every function must be annotated, no implicit `Any`, no untyped calls, and unused `# type: ignore` comments are reported. It's best for new code. Older code can adopt it gradually, per module.

---

### 9. How do you keep code quality high in CI?

**Say:** Run `ruff format --check`, `ruff check` and `mypy` plus the tests on every pull request, and fail the build on errors. Run the same checks locally with pre-commit. Reviews can then focus on design and logic.

---

### 10. What is `@overload` for?

**Say:** It lets you declare several **signatures** for one function when the return type depends on the arguments, e.g. `get(key) -> str | None` but `get(key, default: str) -> str`. Only the final, un-decorated definition actually runs.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
