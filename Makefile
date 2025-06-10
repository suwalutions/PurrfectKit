# Usage:
# make bump part=patch  # or part=minor or part=major

part ?= patch

bump:
	bumpversion $(part)

tag-push:
	git push origin HEAD
	git push origin --tags

release: bump tag-push
