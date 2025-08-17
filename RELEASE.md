# Release & Docker image build guide

This document describes a minimal, reproducible process to build and publish Docker images for FinSight in CI.

Goals

- Produce two kinds of backend images:
  - lightweight/demo image (uses `backend/requirements.light.txt`) for fast deploys and demos
  - full-ML image (uses `backend/requirements.txt`) for production or ML validation
- Tag images with semver or CI run id and push to a registry (GitHub Container Registry or Docker Hub)

Recommended tags

- `ghcr.io/<owner>/finsight-backend:latest` (optional)
- `ghcr.io/<owner>/finsight-backend:vX.Y.Z` (release tag)

Build matrix (example)

- Demo (fast): build with build-arg `USE_LIGHT=1` and env `SKIP_ML=1` baked into image or runtime.
- Full-ML: build with default deps (no `USE_LIGHT`) or `USE_LIGHT=0`.

CI example (GitHub Actions) — high level

1. Checkout code
2. Set up Docker Buildx
3. Authenticate to registry (use `GITHUB_TOKEN` for ghcr or `DOCKER_USERNAME`/`DOCKER_PASSWORD` for Docker Hub stored in secrets)
4. Build and push demo image:

```yaml
# build demo image (light)
- name: Build and push demo image
  uses: docker/build-push-action@v4
  with:
    push: true
    tags: ghcr.io/${{ github.repository_owner }}/finsight-backend:demo-${{ github.run_id }}
    build-args: |
      USE_LIGHT=1
```

5. Optionally build and push full-ML image (slower):

```yaml
- name: Build and push full-ML image
  uses: docker/build-push-action@v4
  with:
    push: true
    tags: ghcr.io/${{ github.repository_owner }}/finsight-backend:${{ github.ref_name }}
    build-args: |
      USE_LIGHT=0
```

Best practices

- Use build cache and layers to avoid long rebuilds. Configure `cache-from`/`cache-to` in actions.
- Keep the demo image small by using `requirements.light.txt` and multi-stage builds.
- Sign or scan images in CI if you require artifact provenance.

Release steps (manual)

1. Bump the version in a `VERSION` file or tag your commit `vX.Y.Z`.
2. Create a GitHub release (or attach a tag) and let CI produce and push images tagged with that version.
3. Verify images by pulling in a staging cluster or running locally with `docker run`.

Rollback

- If a release fails, re-tag a previously-known-good image and update deployment to use the prior tag.

That's it — if you want, I can generate a complete GitHub Actions workflow snippet that builds and pushes both images with caching and optional platform matrix.

# Release & Docker image publishing

This project publishes Docker images for reproducible releases. Use CI to build and push images.

Local image build (backend):

```bash
# from repo root
docker build -f Dockerfile.backend -t finsight-backend:local .
# run in demo mode
docker run --rm -e SKIP_ML=1 -p 5002:5002 finsight-backend:local
```

Publishing from CI (recommended):

- Build images in CI with versioned tags (e.g. `v1.2.0`, `latest`).
- Push images to your container registry (Docker Hub, GitHub Container Registry, etc.).
- Attach release notes to the GitHub Release and include the image tags and digest.

Tagging convention:

- Use semantic version tags: `vMAJOR.MINOR.PATCH`.
- Use `latest` for the most recent stable release.

Notes:

- Use `requirements.light.txt` in CI to speed up builds and tests when you do not need full ML training in CI pipelines.
- For production images with ML models pre-trained, bake model artifacts into the image and ensure license compliance for model artifacts.
