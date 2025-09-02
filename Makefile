.PHONY: help build test clean deploy push-image

# Variables
IMAGE_NAME = elos-google-search-mcp
REGISTRY = quay.io/elostech
FULL_IMAGE_NAME = $(REGISTRY)/$(IMAGE_NAME)
TAG = latest

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build the Docker image
	podman build -t $(IMAGE_NAME):$(TAG) .

test: ## Test the image locally
	podman run --rm -p 8000:8000 \
		-e GOOGLE_API_KEY="test-key" \
		-e GOOGLE_CSE_ID="test-id" \
		$(IMAGE_NAME):$(TAG)

clean: ## Clean up local images
	podman rmi $(IMAGE_NAME):$(TAG) || true
	podman rmi $(FULL_IMAGE_NAME):$(TAG) || true

tag: ## Tag the image for registry
	podman tag $(IMAGE_NAME):$(TAG) $(FULL_IMAGE_NAME):$(TAG)

push-image: tag ## Push the image to Quay.io
	podman push $(FULL_IMAGE_NAME):$(TAG)

deploy: ## Deploy to Kubernetes
	kubectl apply -k kubernetes/

undeploy: ## Remove from Kubernetes
	kubectl delete -k kubernetes/

logs: ## View pod logs
	kubectl logs -l app=$(IMAGE_NAME) -f

status: ## Check deployment status
	kubectl get pods -l app=$(IMAGE_NAME)
	kubectl get services -l app=$(IMAGE_NAME)

install-deps: ## Install Python dependencies
	pip install -e .

run-local: ## Run the server locally
	python -m elos_google_search_mcp.server

build-and-push: build push-image ## Build and push the image

all: build push-image deploy ## Build, push, and deploy
