# Usage:
# make release SemVer=patch
# make release SemVer=minor
# make release SemVer=major

SemVer ?= patch

check-clean:
	@git diff --quiet || (echo "Working tree is not clean. Commit or stash changes first." && exit 1)
	@git diff --cached --quiet || (echo "Index has staged changes. Commit or reset them first." && exit 1)

bump:
	VERSION := $(shell bumpversion --dry-run --list $(SemVer) | grep new_version= | sed -r s,"^.*=",,)
	@echo "Bumping version ($(SemVer)) to $(VERSION)"
	bumpversion --allow-dirty $(SemVer)

tag-push:
	@git push origin HEAD
	@git push origin --tags

latest-tag:
	@if ! echo "patch minor major" | grep -qw "$(SemVer)"; then \
		echo "Skipping 'latest' tag update for SemVer=$(SemVer)"; \
		exit 0; \
	fi
	@if git rev-parse "refs/tags/latest" >/dev/null 2>&1; then \
		echo "Removing existing 'latest' tag..."; \
		git tag -d latest; \
		git push origin :refs/tags/latest; \
	fi
	@echo "Creating new 'latest' tag at current commit..."
	@git tag latest
	@git push origin latest

release: check-clean bump tag-push latest-tag
	@echo "Release $(VERSION) completed and 'latest' tag updated."

# Usage:
# make tag TAG=test
# make tag TAG=docs
# make tag TAG=latest

ALLOWED_TAGS := docs test latest
TAG ?=

.PHONY: tag check-tag

check-tag:
	@if [ -z "$(TAG)" ]; then \
		echo "Error: TAG is required. Usage: make tag TAG=docs|test|latest"; \
		exit 1; \
	fi
	@if ! echo "$(ALLOWED_TAGS)" | grep -qw "$(TAG)"; then \
		echo "Error: Invalid TAG '$(TAG)'. Allowed tags are: $(ALLOWED_TAGS)"; \
		exit 1; \
	fi

tag: check-tag
	@if git rev-parse "refs/tags/$(TAG)" >/dev/null 2>&1; then \
		echo "Removing local tag '$(TAG)'..."; \
		git tag -d $(TAG); \
	else \
		echo "Local tag '$(TAG)' does not exist."; \
	fi
	@if git ls-remote --tags origin | grep -q "refs/tags/$(TAG)$$"; then \
		echo "Removing remote tag '$(TAG)'..."; \
		git push origin :refs/tags/$(TAG); \
	else \
		echo "Remote tag '$(TAG)' does not exist."; \
	fi
	@echo "Creating tag '$(TAG)' at current commit..."
	git tag $(TAG)
	@echo "Pushing tag '$(TAG)' to remote..."
	git push origin $(TAG)


# Usage
# make image-build   # Build the image
# make image-save    # Save the image as a tarball
# make image-clean   # Remove build cache
# make image-run     # Run the container

IMAGE_NAME := purrfectkit
IMAGE_TAG := latest
TAR_NAME := $(IMAGE_NAME)_$(IMAGE_TAG).tar

# 1. Build Docker image
.PHONY: image-build
image-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

# 2. Save Docker image to a tar file
.PHONY: image-save
image-save:
	docker save -o $(TAR_NAME) $(IMAGE_NAME):$(IMAGE_TAG)

# 3. Clean Docker build cache (dangling images and cache)
.PHONY: image-clean
image-clean:
	docker builder prune -f
	docker image prune -f

# 4. Run Docker image
.PHONY: image-run
image-run:
	docker run --rm -it $(IMAGE_NAME):$(IMAGE_TAG)
