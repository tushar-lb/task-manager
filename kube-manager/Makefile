DOCKER_HUB_REPO?=tusharraut
DOCKER_HUB_REGISTRY_IMAGE?=kube-manager
DOCKER_HUB_REGISTRY_TAG?=1.0.0

REGISTRY_IMG=$(DOCKER_HUB_REPO)/$(DOCKER_HUB_REGISTRY_IMAGE):$(DOCKER_HUB_REGISTRY_TAG)


BASE_DIR    := $(shell git rev-parse --show-toplevel)
GIT_SHA     := $(shell git rev-parse --short HEAD)
BIN         :=$(BASE_DIR)/bin

LDFLAGS += "-s -w"
BUILD_OPTIONS := -ldflags=$(LDFLAGS)

container-deploy:
	@echo "Building container: docker build --tag $(REGISTRY_IMG) -f Dockerfile ."
	sudo docker build --tag $(REGISTRY_IMG) -f Dockerfile .
	sudo docker push $(REGISTRY_IMG)