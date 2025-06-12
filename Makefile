# Releasing new versions
# Usage: make release v-part=patch  # or v-part=minor or v-part=major

v-part ?= patch
VERSION := $(shell bumpversion --dry-run --list $(v-part) | grep new_version= | sed -r s,"^.*=",,)

check-clean:
	@git diff --quiet || (echo "Working tree is not clean. Commit or stash changes first." && exit 1)
	@git diff --cached --quiet || (echo "Index has staged changes. Commit or reset them first." && exit 1)

bump:
	@echo "Bumping version ($(v-part)) to $(VERSION)"
	bumpversion --allow-dirty $(v-part)

changelog:
	@echo "Generating changelog..."
	@git log $(VERSION)^..HEAD --pretty=format:"* %s (%an)" > CHANGELOG.md || echo "Failed to generate changelog"
	@git add CHANGELOG.md
	@git commit -m "Update changelog for version $(VERSION)"

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

release: check-clean bump changelog tag-push latest-tag
	@echo "Release $(VERSION) completed and 'latest' tag updated."

# Deploying new documentation
# Usage: make tag TAG=docs

ALLOWED_TAGS := docs
TAG ?=

check-tag:
	@if [ -z "$(TAG)" ]; then \
		echo "Error: TAG is required. Usage: make tag TAG=docs"; \
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

.PHONY: release check-clean bump changelog tag-push tag check-tag