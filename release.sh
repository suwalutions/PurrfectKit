#!/bin/bash
# release.sh
# Usage: ./release.sh patch|minor|major (default: patch)

set -e

V_PART=${1:-patch}
VERSION=$(bumpversion --dry-run --list "$V_PART" | grep new_version= | sed -r s,"^.*=",,)

# Check if working tree is clean
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Working tree or index is not clean. Commit or stash changes first."
    exit 1
fi

# Bump version
echo "Bumping version ($V_PART) to $VERSION"
bumpversion --allow-dirty "$V_PART"

# Generate changelog
echo "Generating changelog..."
git log "${VERSION}^"..HEAD --pretty=format:"* %s (%an)" > CHANGELOG.md || echo "Failed to generate changelog"
git add CHANGELOG.md
git commit -m "Update changelog for version $VERSION"

# Push changes
git push origin HEAD
git push origin --tags

echo "Release $VERSION completed."
