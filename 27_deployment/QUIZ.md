# Python Pro – Module 27 Knowledge Check
**Docker, CI/CD & deploying to Azure**

The answer key is at the bottom, and each answer says which file to revisit.

---

**1. What problem does a container image solve?**
- A) It makes Python faster
- B) The app and all its dependencies are packaged together, so it runs the same everywhere
- C) It replaces tests
- D) It encrypts code

**2. Why copy `requirements.txt` and install BEFORE copying the code?**
- A) Alphabetical order
- B) Docker caches layers: changing code doesn't re-install every package
- C) It's required syntax
- D) Smaller image

**3. Why a multi-stage build?**
- A) Faster tests
- B) Build tools stay in the build stage; the final image is small and contains only what runs
- C) To run two apps
- D) It's required by Azure

**4. Why `USER appuser` instead of root?**
- A) Speed
- B) If the app is compromised, the attacker isn't root inside the container
- C) Logging
- D) Azure needs it

**5. Where do secrets like the DB password belong?**
- A) In the Dockerfile `ENV`
- B) In platform secrets / Key Vault, injected at runtime as env vars
- C) In git
- D) In the image name

**6. Liveness vs readiness probes?**
- A) Same thing
- B) Liveness: is the process alive (restart it if not); readiness: can it serve traffic now (route traffic or not)
- C) Readiness restarts the app
- D) Liveness checks the database

**7. Why log one JSON object per line to stdout?**
- A) Prettier
- B) The platform collects stdout, and JSON is searchable in Azure Monitor / Log Analytics
- C) Files are not allowed
- D) Smaller logs

**8. What does `docker compose up` give you locally?**
- A) A cloud deployment
- B) The API plus Postgres plus Redis, wired together with one command
- C) Only the database
- D) Tests

**9. In the CI pipeline, why does `deploy` have `needs: test`?**
- A) Alphabetical order
- B) Nothing is deployed unless lint, type checks and tests pass
- C) To run in parallel
- D) To save money

**10. What does OIDC (`id-token: write`) give the Azure login in GitHub Actions?**
- A) Faster builds
- B) Passwordless, short-lived credentials: no long-lived secret stored in GitHub
- C) Free Azure credits
- D) Docker caching

**11. Why tag images with the git commit SHA instead of `latest`?**
- A) Shorter names
- B) You always know exactly which code is running, and rollbacks are easy
- C) Docker requires it
- D) Smaller images

**12. Why gunicorn with uvicorn workers in production?**
- A) It's required by FastAPI
- B) Several worker processes use all CPU cores, and crashed workers are restarted
- C) It adds HTTPS
- D) It's a database driver

**13. What does `--min-replicas 0` on Azure Container Apps do?**
- A) Deletes the app
- B) Scales to zero when idle (you pay nothing), and starts on the next request
- C) Disables HTTPS
- D) Runs one replica forever

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | B | `Dockerfile` |
| 2 | B | `Dockerfile` |
| 3 | B | `Dockerfile` |
| 4 | B | `Dockerfile` |
| 5 | B | `azure/deploy.sh` |
| 6 | B | `app/main.py` |
| 7 | B | `app/main.py` |
| 8 | B | `docker-compose.yml` |
| 9 | B | `github-actions/ci-cd.yml` |
| 10 | B | `github-actions/ci-cd.yml` |
| 11 | B | `github-actions/ci-cd.yml` |
| 12 | B | `Dockerfile` |
| 13 | B | `azure/deploy.sh` |

</details>

---

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
