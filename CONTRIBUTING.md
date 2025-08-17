# Contributing to FinSightAI

Thank you for your interest in contributing to FinSightAI! We welcome all contributions: features, bug fixes, documentation, and UI/UX improvements.

## How to Contribute

1. **Fork the repository** and create a feature branch from `main`.
2. **Describe your changes** clearly in commit messages and pull requests.
3. **Test your code** (frontend and backend) before submitting.
4. **Submit a pull request** with a summary of your changes and screenshots if UI-related.
5. For major changes, open an issue first to discuss your proposal.

## Code Style & Guidelines

- **Frontend (React):**
  - Use [Prettier](https://prettier.io/) for formatting
  - Follow [Ant Design](https://ant.design/docs/spec/introduce) UI patterns
  - Use functional components and hooks
  - Keep code modular and well-commented
- **Backend (Python/Flask):**
  - Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) style
  - Document endpoints and ML logic
  - Write clear, maintainable code

# Contributing

Thanks for contributing to FinSight. This document gives a concise, developer-ready workflow.

1. Local setup

- Follow `README.md` to create the backend venv and install frontend deps.

2. Tests & linting

- Backend (pytest):
  ```bash
  cd backend
  source .venv/bin/activate
  pip install pytest
  pytest -q
  ```
- Frontend (jest/eslint):
  ```bash
  cd frontend
  npm ci
  npm test
  npm run lint   # if configured
  ```

3. Commit / branch conventions

- Branches: `feat/<short>`, `fix/<short>`, `chore/<short>`.
- Commit messages: use Conventional Commits (e.g. `feat: add rule editor`).

4. Pull request requirements

- Tests and lint must pass locally.
- Include a short description, how to test, and screenshots for UI changes.

## How to open a reproducible PR

Follow this checklist to make your PR easy to review and reproduce locally:

- Start from an up-to-date `main` branch: `git checkout main && git pull`
- Create a feature branch: `git checkout -b feat/short-description`
- Keep changes small and focused (one logical change per PR)
- Add or update tests that exercise the new behavior
- Run the full local test steps and include the exact commands in the PR description
  ```bash
  cd backend
  source .venv/bin/activate
  export ANOMALY_CONTAMINATION=0.05
  pytest -q
  # frontend
  cd ../frontend
  npm ci
  npm test --silent
  ```
- Provide a reproducible dev environment note if special setup is required (Python version, optional prebuilt model artifacts)
- Include a short "how to test locally" section in the PR description (commands, env vars)
- Use the PR template and reference any related issues

5. Code style

- Frontend: use Prettier and ESLint rules in the repo.
- Backend: follow PEP8; use `flake8` for CI checks if added.

6. Adding ML models or categories

- Place model code under `backend/models/` and expose `train()`/`predict()`.
- Add unit tests under `backend/tests/` and update `backend/models/README.md` with training steps.

7. Security & secrets

- Never commit secrets. Use environment variables or CI secret stores.

8. Reporting issues

- Open an issue with reproducible steps and attach logs if applicable.

By contributing you agree your contribution will be released under the MIT License.

## Testing anomaly sensitivity

When writing or running backend tests that exercise anomaly detection, you can control the `IsolationForest` sensitivity via the `ANOMALY_CONTAMINATION` environment variable.

- Recommended for tests: set a small, deterministic contamination value to make tests stable. e.g. `ANOMALY_CONTAMINATION=0.05`.
- CI: set the env var in the workflow or test runner to a known value so tests are reproducible across machines.

Example (local pytest run):

```bash
cd backend
source .venv/bin/activate
export ANOMALY_CONTAMINATION=0.05
pytest -q
```

The backend clamps invalid values (outside (0, 0.5)) to the default of `0.2`, so prefer values in the valid range for test clarity.
