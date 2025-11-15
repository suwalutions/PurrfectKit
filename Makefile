# =============================================================================
# PURRFECTKIT
# =============================================================================

PKG_NAME        = purrfectkit
REPO_OWNER      = suwalutions
LATEST         ?= true     # tag 'latest' on final release
IMAGE          ?= false    # build Docker
DOCS           ?= false    # rebuild docs
SEM_VERSION    ?= patch    # bump level
BUMP           := uv tool run bump-my-version
CURRENT_VERSION = $(shell $(BUMP) show current_version | sed -E 's/.*= *//')
UPGRADE_VERSION = $(shell $(BUMP) show --increment $(SEM_VERSION) new_version | sed -E 's/.*= *//')

TAG_NAME		?= latest
IMG_TAG			?= latest

# ───── FULL RELEASE ─────
deploy:
	@echo "RELEASE: $(CURRENT_VERSION) → $(UPGRADE_VERSION)"
	@$(BUMP) bump $(SEM_VERSION)
	@git push origin HEAD --tags
	@[ "$(LATEST)" = "true" ] && make git-tag TAG_NAME=latest || true
	@[ "$(IMAGE)" = "true" ] && make docker-img IMG_TAG=v$(UPGRADE_VERSION) || true
	@[ "$(DOCS)" = "true" ] && make git-tag TAG_NAME=docs || true
	@echo ""
	@echo "RELEASE COMPLETE"
	@echo "PyPI: https://pypi.org/project/$(PKG_NAME)/$(UPGRADE_VERSION)/"
	@echo "Docker: ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(IMG_TAG)"
	@echo "Docs: https://$(REPO_OWNER).github.io/PurrfectKit/"

# ───── TAG UPDATE ─────
git-tag:
	@echo "Updating tag: $(TAG_NAME)"
	@git tag -d $(TAG_NAME) 2>/dev/null || true
	@git push origin :refs/tags/$(TAG_NAME) 2>/dev/null || true
	@git tag -f $(TAG_NAME)
	@git push -f origin $(TAG_NAME)
	@echo "Tag '$(TAG_NAME)' → updated"

# ───── DOCKER BUILD & PUSH ─────
docker-img:
	@echo "Building Docker → $(IMG_TAG)"
	@docker build -t $(PKG_NAME):$(IMG_TAG) .
	@echo $$GITHUB_TOKEN | docker login ghcr.io -u $$GITHUB_ACTOR --password-stdin
	@echo $$DOCKERHUB_TOKEN | docker login -u $$DOCKERHUB_USERNAME --password-stdin
	@docker tag $(PKG_NAME):$(IMG_TAG) ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(IMG_TAG)
	@docker tag $(PKG_NAME):$(IMG_TAG) $$DOCKERHUB_USERNAME/$(PKG_NAME):$(IMG_TAG)
	@docker push ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(IMG_TAG)
	@docker push $$DOCKERHUB_USERNAME/$(PKG_NAME):$(IMG_TAG)
	@echo "DOCKER LIVE → ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(IMG_TAG)"
	@echo "DOCKER LIVE → docker.io/$$DOCKERHUB_USERNAME/$(PKG_NAME):$(IMG_TAG)"

# ───── HELP ─────
help:
	@echo "make deploy                     		# final release"
	@echo "make deploy SEM_VERSION=minor   		# bump minor"
	@echo "make deploy LATEST=false        		# no 'latest' tag"
	@echo "make deploy IMAGE=true          		# + Docker"
	@echo "make deploy DOCS=true           		# + docs rebuild"
	@echo "make deploy IMAGE=true DOCS=true LATEST=false  	# full control"

.PHONY: deploy git-tag docker-img help
