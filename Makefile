SEM_VERSION	?= patch
VERSION		= $(shell grep '^version' pyproject.toml | head -n1 | cut -d'"' -f2 | tr -d ' ')
TAG			= v$(VERSION)
PKG_NAME	= purrfectkit
REPO_OWNER	= suwalutions

.PHONY: bump-version wait-pypi build-docs wait-docs docker-images deploy deploy-lite help

bump-version:
	@bumpversion --allow-dirty $(SEM_VERSION)
	@git push origin HEAD --tags
	@git tag -f latest
	@git push -f origin latest
	@echo "Tagged $(TAG) + latest"

wait-pypi:
	@echo "Waiting for PyPI..."
	@sleep 15
	@while ! curl -fs https://pypi.org/pypi/$(PKG_NAME)/$(VERSION)/json > /dev/null; do \
		echo "Still building..."; sleep 8; \
	done
	@echo "PYPI LIVE → https://pypi.org/project/$(PKG_NAME)/$(VERSION)/"

build-docs:
	@git tag -d docs 2>/dev/null || true
	@git push origin :refs/tags/docs 2>/dev/null || true
	@git tag docs
	@git push origin docs
	@echo "Docs rebuild triggered"

wait-docs:
	@echo "Waiting for docs..."
	@while ! curl -fs https://$(REPO_OWNER).github.io/PurrfectKit/ > /dev/null; do sleep 10; done
	@echo "DOCS LIVE → https://$(REPO_OWNER).github.io/PurrfectKit/"

docker-images:
	@docker build -t $(PKG_NAME):$(TAG) -t $(PKG_NAME):latest .
	@echo $$DOCKERHUB_TOKEN | docker login -u $$DOCKERHUB_USERNAME --password-stdin
	@echo $$GITHUB_TOKEN | docker login ghcr.io -u $$GITHUB_ACTOR --password-stdin
	@docker tag $(PKG_NAME):$(TAG) ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(TAG)
	@docker tag $(PKG_NAME):$(TAG) $$DOCKERHUB_USERNAME/$(PKG_NAME):$(TAG)
	@docker push ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(TAG)
	@docker push $$DOCKERHUB_USERNAME/$(PKG_NAME):$(TAG)
	@echo "DOCKER LIVE → ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(TAG)"

deploy:
	@make bump-version SEM_VERSION=$(SEM_VERSION)
	@make wait-pypi
	@make build-docs
	@make wait-docs
	@make docker-images
	@echo ""
	@echo "MEOW EMPIRE HAS ASCENDED"
	@echo "Version : $(VERSION)"
	@echo "PyPI    : https://pypi.org/project/$(PKG_NAME)/$(VERSION)/"
	@echo "Docs    : https://$(REPO_OWNER).github.io/PurrfectKit/"
	@echo "Docker  : ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(TAG)"
	@echo ""

deploy-lite:
	@make bump-version SEM_VERSION=$(SEM_VERSION)
	@make wait-pypi
	@make build-docs
	@make wait-docs
	@echo ""
	@echo "MEOW EMPIRE HAS ASCENDED"
	@echo "Version : $(VERSION)"
	@echo "PyPI    : https://pypi.org/project/$(PKG_NAME)/$(VERSION)/"
	@echo "Docs    : https://$(REPO_OWNER).github.io/PurrfectKit/"
	@echo ""

help:
	@echo "make deploy					# Full atomic release"
	@echo "make deploy SEM_VERSION=major			# Override bump level (patch/minor/major)"
	@echo "make deploy-lite				# deploy without Docker"
	@echo "make bump-version				# tags latest + vX.Y.Z"
	@echo "make build-docs					# deploy documentation only"
	@echo "make docker-images				# deploy docker images only"
