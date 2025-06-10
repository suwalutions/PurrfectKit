# Makefile for releasing new versions
# Usage:
# make release v-part=patch  # or v-part=minor or v-part=major

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

release: check-clean bump changelog tag-push
	@echo "Release $(VERSION) completed."
