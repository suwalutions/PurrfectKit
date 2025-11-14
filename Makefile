# =============================================================================
# PURRFECTKIT — COMPLETE DEPLOY SYSTEM (dev/alpha/beta/rc/final)
# All versions. All workflows. One command each.
# =============================================================================

PKG_NAME    = purrfectkit
REPO_OWNER  = suwalutions
IMAGE       ?= false    # default: no Docker
DOCS        ?= true     # default: with Documentation
VERSION     ?=
TAG         ?=

# Refresh VERSION and TAG
_get-version:
	@$(eval VERSION = $(shell grep '^version' pyproject.toml | head -n1 | cut -d'"' -f2 | tr -d ' '))
	@$(eval TAG = v$(VERSION))
	@echo "TAG: $(TAG)"

# ───── INTERNAL: Ensure pre-release exists ─────
_init-pre-release:
	@CURRENT_VERSION=$(shell grep '^version' pyproject.toml | head -n1 | cut -d'"' -f2); \
	if ! echo $$CURRENT_VERSION | grep -E -q '\-(dev|alpha|beta|rc|final)\.[0-9]+'; then \
		echo "Initializing pre-release suffix..."; \
		bumpversion --new-version "$$CURRENT_VERSION-dev.0" patch; \
	fi

# ───── 1. DEV DEPLOY ─────
deploy-dev:
	@echo "DEV DEPLOY → internal only"
	@make _get-version
	@make _init-pre-release
	@bumpversion dev
	@make _get-version
	@git push origin HEAD --tags
	@echo "DEV TAG: $(TAG)"
	@[ "$(IMAGE)" = "true" ] && make _docker TAG=$(TAG) || true
	@[ "$(DOCS)" = "true" ] && make build-docs && make wait-docs || true
	@echo "DEV BUILD READY"

# ───── 2. ALPHA DEPLOY → TestPyPI ─────
deploy-alpha:
	@echo "ALPHA DEPLOY → TestPyPI"
	@make _get-version
	@make _init-pre-release
	@bumpversion alpha
	@make _get-version
	@git push origin HEAD --tags
	@echo "ALPHA TAG: $(TAG)"
	@make wait-test-pypi
	@[ "$(IMAGE)" = "true" ] && make _docker TAG=$(TAG) || true
	@[ "$(DOCS)" = "true" ] && make build-docs && make wait-docs || true
	@echo "ALPHA COMPLETE"

# ───── 3. BETA DEPLOY → TestPyPI ─────
deploy-beta:
	@echo "BETA DEPLOY → TestPyPI"
	@make _get-version
	@make _init-pre-release
	@bumpversion beta
	@make _get-version
	@git push origin HEAD --tags
	@echo "BETA TAG: $(TAG)"
	@make wait-test-pypi
	@[ "$(IMAGE)" = "true" ] && make _docker TAG=$(TAG) || true
	@[ "$(DOCS)" = "true" ] && make build-docs && make wait-docs || true
	@echo "BETA COMPLETE"

# ───── 4. RC DEPLOY → TestPyPI ─────
deploy-rc:
	@echo "RC DEPLOY → TestPyPI"
	@make _get-version
	@make _init-pre-release
	@bumpversion rc
	@make _get-version
	@git push origin HEAD --tags
	@echo "RC TAG: $(TAG)"
	@make wait-test-pypi
	@[ "$(IMAGE)" = "true" ] && make _docker TAG=$(TAG) || true
	@[ "$(DOCS)" = "true" ] && make build-docs && make wait-docs || true
	@echo "RC COMPLETE"

# ───── 5. FINAL DEPLOY → PyPI + latest ─────
deploy:
	@echo "FINAL DEPLOY → PyPI + latest tag"
	@make _get-version
	@make _init-pre-release
	@bumpversion final
	@make _get-version
	@git push origin HEAD --tags
	@git tag -f latest
	@git push -f origin latest
	@echo "FINAL TAG: $(TAG) + latest"
	@make wait-pypi
	@[ "$(IMAGE)" = "true" ] && make _docker TAG=$(TAG) || true
	@[ "$(DOCS)" = "true" ] && make build-docs && make wait-docs || true
	@echo ""
	@echo "FINAL DEPLOY COMPLETE"
	@echo "$(VERSION) → PyPI + Docs"
	@[ "$(IMAGE)" = "true" ] && echo "Docker → ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(TAG)" || true
	@[ "$(DOCS)" = "true" ] && echo "Docs → https://$(REPO_OWNER).github.io/PurrfectKit/" || true

# ───── DOCUMENTATION ─────
build-docs:
	@git tag -d docs 2>/dev/null || true
	@git push origin :refs/tags/docs 2>/dev/null || true
	@git tag docs
	@git push origin docs
	@echo "Docs rebuild triggered"

# ───── WAITERS ─────
wait-pypi:
	@echo "Waiting for PyPI..."
	@sleep 15
	@while ! curl -fs https://pypi.org/pypi/$(PKG_NAME)/$(VERSION)/json >/dev/null; do \
		echo "..."; sleep 8; \
	done
	@echo "PYPI → https://pypi.org/project/$(PKG_NAME)/$(VERSION)/"

wait-test-pypi:
	@echo "Waiting for TestPyPI..."
	@sleep 15
	@while ! curl -fs https://test.pypi.org/pypi/$(PKG_NAME)/$(VERSION)/json >/dev/null; do \
		echo "..."; sleep 8; \
	done
	@echo "TESTPYPI → https://test.pypi.org/project/$(PKG_NAME)/$(VERSION)/"

wait-docs:
	@echo "Waiting for docs..."
	@while ! curl -fs https://$(REPO_OWNER).github.io/PurrfectKit/ >/dev/null; do sleep 10; done
	@echo "DOCS → https://$(REPO_OWNER).github.io/PurrfectKit/"

# ───── INTERNAL: DOCKER BUILD & PUSH ─────
_docker:
	@echo "Building Docker → $(TAG)"
	@docker build -t $(PKG_NAME):$(TAG) .
	@echo $$DOCKERHUB_TOKEN | docker login -u $$DOCKERHUB_USERNAME --password-stdin
	@echo $$GITHUB_TOKEN | docker login ghcr.io -u $$GITHUB_ACTOR --password-stdin
	@docker tag $(PKG_NAME):$(TAG) ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(TAG)
	@docker tag $(PKG_NAME):$(TAG) $$DOCKERHUB_USERNAME/$(PKG_NAME):$(TAG)
	@docker push ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(TAG)
	@docker push $$DOCKERHUB_USERNAME/$(PKG_NAME):$(TAG)
	@echo "DOCKER → ghcr.io/$(REPO_OWNER)/$(PKG_NAME):$(TAG)"

# ───── HELP ─────
help:
	@echo "DEPLOY COMMANDS:"
	@echo "  make deploy IMAGE=true            	# Final → PyPI + Docs + Docker"
	@echo "  make deploy                     	# Final → PyPI + Docs"
	@echo "  make deploy-dev DOCS=false         	# Dev internal only"
	@echo "  make deploy-alpha DOCS=false       	# Alpha → TestPyPI"
	@echo "  make deploy-beta IMAGE=true        	# Beta → TestPyPI + Docs + Docker"
	@echo "  make deploy-rc IMAGE=true          	# RC → TestPyPI + Docs + Docker"
	@echo "  make build-docs                  	# Docs"
	@echo ""
	@echo "  make help                        	# this"

.PHONY: _get-version _init-pre-release deploy-dev deploy-alpha deploy-beta deploy-rc deploy build-docs wait-pypi wait-test-pypi wait-docs _docker help
