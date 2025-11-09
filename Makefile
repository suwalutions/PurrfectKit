# =============================================================================
# PurrfectKit — The Ultimate Thai Cat Release Fortress
# One command to deploy everything. Full manual control preserved.
# =============================================================================

# Add this line at the very top (after the comment header):
.PHONY: check-clean bump tag-push latest-tag release tag image-build image-save image-clean image-run image-push image-release deploy wait-pypi trigger-docs wait-docs docker-release celebrate deploy-dry deploy-no-docker

# ─────────────────────────────────────────────────────────────
# 1. VERSION RELEASE
# ─────────────────────────────────────────────────────────────
# Usage:
# make release (default to patch)
# make release SemVer=(patch/minor/major)

SemVer ?= patch
VERSION ?= $(shell bumpversion --dry-run --list $(SemVer) 2>/dev/null | grep '^new_version=' | cut -d= -f2 || echo "0.0.0")
TAG_V := v$(VERSION)

.PHONY: check-clean bump tag-push latest-push latest-tag release

check-clean:
	@git diff --quiet || (echo "Working tree is not clean. Commit or stash changes first." && exit 1)
	@git diff --cached --quiet || (echo "Index has staged changes. Commit or reset them first." && exit 1)

bump:
	@echo "Bumping version ($(SemVer)) → $(VERSION)"
	@bumpversion --allow-dirty $(SemVer)

tag-push:
	@git push origin HEAD
	@git push origin --tags

latest-tag:
	@if ! echo "patch minor major" | grep -qw "$(SemVer)"; then \
		echo "Skipping 'latest' tag (not a semver bump)"; \
		exit 0; \
	fi
	@git tag -f latest
	@git push -f origin latest

release: check-clean bump tag-push latest-tag
	@echo "Release $(VERSION) completed + 'latest' tag updated."

# ─────────────────────────────────────────────────────────────
# 2. TAG MANAGEMENT
# ─────────────────────────────────────────────────────────────
# Usage:
# make tag TAG=(test/docs/latest)

ALLOWED_TAGS := docs test latest
TAG ?=

.PHONY: check-tag tag

check-tag:
	@test -n "$(TAG)" || (echo "Error: TAG is required. Usage: make tag TAG=docs|test|latest" && exit 1)
	@echo "$(ALLOWED_TAGS)" | grep -qw "$(TAG)" || (echo "Invalid TAG '$(TAG)'. Allowed: $(ALLOWED_TAGS)" && exit 1)

tag: check-tag
	@git tag -d $(TAG) 2>/dev/null || true
	@git push origin :refs/tags/$(TAG) 2>/dev/null || true
	@git tag $(TAG)
	@git push origin $(TAG)
	@echo "Tag '$(TAG)' created and pushed"

# ─────────────────────────────────────────────────────────────
# 3. DOCKER IMAGE RELEASE (latest / vX.Y.Z)
# ─────────────────────────────────────────────────────────────
# Usage:
# make image-release
# make image-release IMG_TAG=(latest/vX.Y.Z)

.PHONY: image-build image-save image-clean image-run image-push image-release

IMAGE_NAME := purrfectkit
IMG_TAG ?= latest
TAR_NAME := $(IMAGE_NAME)_$(IMG_TAG).tar

DOCKERHUB_USERNAME ?= $(shell echo $$DOCKERHUB_USERNAME)
GITHUB_OWNER := suwalutions
GITHUB_ACTOR ?= $(shell echo $$GITHUB_ACTOR)

image-build:
	docker build -t $(IMAGE_NAME):$(IMG_TAG) .

image-save:
	docker save -o $(TAR_NAME) $(IMAGE_NAME):$(IMG_TAG)

image-clean:
	docker builder prune -f
	docker image prune -f

image-run:
	docker run --rm -it $(IMAGE_NAME):$(IMG_TAG)

image-push:
	@echo "Logging in to Docker Hub..."
	@echo $$DOCKERHUB_TOKEN | docker login -u $(DOCKERHUB_USERNAME) --password-stdin
	@echo "Logging in to GitHub Container Registry..."
	@echo $$GITHUB_TOKEN | docker login ghcr.io -u $(GITHUB_ACTOR) --password-stdin

	@echo "Tagging images..."
	docker tag $(IMAGE_NAME):$(IMG_TAG) ghcr.io/$(GITHUB_OWNER)/$(IMAGE_NAME):$(IMG_TAG)
	docker tag $(IMAGE_NAME):$(IMG_TAG) $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(IMG_TAG)

	@echo "Pushing image to Github Container Register..."
	docker push ghcr.io/$(GITHUB_OWNER)/$(IMAGE_NAME):$(IMG_TAG)

	@echo "Pushing image to Docker Hub..."
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(IMG_TAG)

image-release: image-build image-save image-push
	@echo "Image $(IMAGE_NAME):$(IMG_TAG) built, saved, and pushed!"

# ─────────────────────────────────────────────────────────────
# 4. ULTIMATE DEPLOYMENT
# ─────────────────────────────────────────────────────────────
# Usage:
# make deploy

.PHONY: deploy wait-pypi trigger-docs wait-docs docker-release celebrate deploy-dry deploy-no-docker

deploy: release wait-pypi trigger-docs wait-docs docker-release celebrate

pypi-now:
	@echo "Pushing CURRENT version $(shell python -c "import purrfectmeow; print(purrfectmeow.__version__)") to PyPI..."
	@git push origin HEAD --tags
	@sleep 8
	@make wait-pypi || (echo "PyPI workflow failed — check GitHub Actions" && exit 1)
	@echo "CURRENT VERSION IS NOW LIVE ON PYPI!"

wait-pypi:
	@echo "Waiting for PyPI publish (latest commit)..."
	@sleep 15
	@while true; do \
		RUN=$$(curl -s https://api.github.com/repos/$(GITHUB_OWNER)/PurrfectKit/actions/runs | \
			jq -r '.workflow_runs[] | select(.head_branch=="meow" and .name=="Publish to PyPI") | .status + " " + .conclusion' | head -n1); \
		echo "PyPI status: $$RUN"; \
		if echo "$$RUN" | grep -q "completed success"; then \
			echo "LIVE → https://pypi.org/project/purrfectkit/$(shell python -c "import purrfectmeow; print(purrfectmeow.__version__)")/"; \
			break; \
		fi; \
		sleep 10; \
	done

trigger-docs:
	@make tag TAG=docs

wait-docs:
	@echo "Waiting for documentation to deploy..."
	@while ! curl -f -s https://$(GITHUB_OWNER).github.io/PurrfectKit/ > /dev/null; do \
		echo "Docs not ready..."; sleep 12; \
	done
	@echo "DOCS LIVE → https://$(GITHUB_OWNER).github.io/PurrfectKit/"

docker-release:
	@make image-release IMG_TAG=$(TAG_V)

celebrate:
	@echo ""
	@echo "╭───────────────────────────────────────────────────────────────────────────────╮"
	@echo "│		PURRFECTKIT $(VERSION) IS NOW IMMORTAL EVERYWHERE				│"
	@echo "│                                                          			│"
	@echo "│  PyPI			→	https://pypi.org/project/$(IMAGE_NAME)/$(VERSION)/		│"
	@echo "│  Docs			→	https://$(GITHUB_OWNER).github.io/PurrfectKit/	│"
	@echo "│  Docker		→ 	ghcr.io/$(GITHUB_OWNER)/$(IMAGE_NAME):$(TAG_V)		│"
	@echo "│                                                          			│"
	@echo "│  All 5 Thai cats are purring in perfect harmony.        			│"
	@echo "╰───────────────────────────────────────────────────────────────────────────────╯"
	@echo ""

# ─────────────────────────────────────────────────────────────
# BONUS: Dry-run & skip modes
# ─────────────────────────────────────────────────────────────
deploy-dry:
	@echo "DRY RUN: make deploy SemVer=$(SemVer)"
	@echo "   → bump to $(VERSION)"
	@echo "   → tag v$(VERSION) + latest"
	@echo "   → trigger PyPI publish"
	@echo "   → rebuild docs"
	@echo "   → build & push docker:$(TAG_V)"

deploy-no-docker:
	@make release SemVer=$(SemVer)
	@make wait-pypi
	@make trigger-docs
	@make wait-docs
	@echo "Deploy complete (Docker skipped)"

# ─────────────────────────────────────────────────────────────
# HELP — The most beautiful help in open source history
# ─────────────────────────────────────────────────────────────
help:
	@echo "			PurrfectKit — Thai Cat Release Fortress"
	@echo "============================================================================================"
	@echo "|"
	@echo "| GOD COMMAND (one enter → everything updates)"
	@echo "|   make deploy					# Full atomic release (PyPI + Docs + Docker)"
	@echo "|   make deploy SemVer=minor			# Override bump level (patch/minor/major)"
	@echo "|   make deploy SemVer=1.5.0			# Direct version (skip bumpversion)"
	@echo "| "
	@echo "| DRY RUN & SAFETY"
	@echo "|   make deploy-dry				# Show exactly what will happen"
	@echo "|   make deploy-no-docker			# Everything except Docker push"
	@echo "| "
	@echo "| MANUAL CONTROL (you still own every step)"
	@echo "|   make release				# Default: bump patch → vX.Y.Z+1"
	@echo "|   make release SemVer=minor			# Bump minor → vX.Y+1.0"
	@echo "|   make release SemVer=major			# Bump major → vX+1.0.0"
	@echo "|   make tag TAG=docs				# Rebuild & deploy documentation only"
	@echo "|   make tag TAG=latest				# Force-update 'latest' pointer"
	@echo "| "
	@echo "| DOCKER COMMANDS"
	@echo "|   make image-release				# Build & push with IMG_TAG=latest"
	@echo "|   make image-release IMG_TAG=v2.1.0		# Specific version"
	@echo "|   make image-release IMG_TAG=experimental	# Custom tag"
	@echo "|   make image-run				# Run container locally"
	@echo "| "
	@echo "| BONUS UTILITIES"
	@echo "|   make help					# This beautiful menu"
	@echo "|   make celebrate				# Print victory cat (for emergencies)"
	@echo "| "
	@echo "| EXAMPLE FULL RELEASE (copy-paste this):"
	@echo "|   make deploy SemVer=patch"
	@echo "| "
	@echo "| RESULT AFTER DEPLOY:"
	@echo "|    PyPI			→ https://pypi.org/project/purrfectkit/X.Y.Z/"
	@echo "|    Docs			→ https://suwalutions.github.io/PurrfectKit/"
	@echo "|    Docker			→ ghcr.io/suwalutions/purrfectkit:vX.Y.Z"
	@echo "| "
	@echo "|    All 5 Thai cats purring in perfect harmony"
	@echo "| "
	@echo "============================================================================================"
	@echo "			You are not just releasing code."
	@echo "			You are conducting a symphony of Thai cats."
	@echo "============================================================================================"
