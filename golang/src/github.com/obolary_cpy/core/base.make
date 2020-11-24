# platform target of publish, deployment and status
# it can be aws or gcloud. azure is not supported
# note that the aws platform requires AMI credentials (e.g., via Jenkins)
PLATFORM ?= gcloud

# source is the mount point for docker build tools
# it is always set to the local GOPATH and expects a single path (not multiple)
SOURCE ?= $(GOPATH)

# golang builder container
GOLANG ?= golang:1.12

# namespace is the kubernetes deployment namespace
# this is application specific, e.g., xero, listing, etc.
NAMESPACE ?= xero

# node-env is determines the host for the docker build arg, NODE_ENV
# this can be production, develop, or staging/master
# it is optionally used in the Dockerfile, e.g.,
#   ...
#   ARG NODE_ENV
#   ENV NODE_ENV=$NODE_ENV
#   ...
NODE_ENV ?= production

# the number of replicas is based on the node-env setting
# this value is usually set in the child makefile
REPLICAS ?= 1

# initialize TAG
ifeq ($(PLATFORM),aws)
	AWS_REGION ?= $(shell aws configure get region)
ifeq ($(AWS_REGION),)
	AWS_REGION = us-east-1
endif
	AWS_ACCOUNT_ID ?= $(shell aws sts get-caller-identity --region $(AWS_REGION) --query Account --output text)
	AWS_REGISTRY ?= $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
	REGISTRY = $(AWS_REGISTRY)
endif
ifeq ($(PLATFORM),gcloud)
	GOO_ACCOUNT_ID ?= $(shell gcloud config get-value project)
	GOO_REGISTRY ?= gcr.io/$(GOO_ACCOUNT_ID)
	REGISTRY = $(GOO_REGISTRY)
endif
VERSION ?= latest
TAG ?= $(REGISTRY)/$(IMAGE):$(VERSION)

# clean binary
.PHONY: clean
clean:
	@rm -f $(IMAGE)

# build a golang based repo using the default golang container.
# typically the base container would be something like "FROM debian"
# this is the most commonly used build rule, default to this if you're
# unsure which golang build rule to use.
.PHONY: golang_build
golang_build:
	@echo "* BUILD: '"$(IMAGE)"'"
	@rm -f $(IMAGE)
	docker run --rm -v $(SOURCE):$(SOURCE) -v $(HOME):/root -w $(PWD) -e GOPATH=$(GOPATH) -e GO111MODULE=on $(GOLANG) go build -v -o $(IMAGE)
	@echo "* DONE : make golang_build"

# build a golang based repo using the default golang container
# this rule requires that the given container is "FROM scratch"
# this rule is used to build tiny containers
.PHONY: golang_build_scratch
golang_build_scratch:
	@echo "* BUILD: '"$(IMAGE)"'"
	@rm -f $(IMAGE)
	docker run --rm -v $(SOURCE):$(SOURCE) -v $(HOME):/root -w $(PWD) -e GOPATH=$(GOPATH) -e GO111MODULE=on -e CGO_ENABLED=0 -e GOOS=linux $(GOLANG) go build -v -a -ldflags '-extldflags "-static"' -o $(IMAGE)
	@echo "* DONE : make golang_build"

# build a golang based repo using the given docker container
# this rule requires that the given container is "FROM golang:X.Y" or a variant, e.g., "FROM xero-kafka"
# this rule is only used when the developer needs to build other libraries (e.g., gcc) besides the go code
# e.g., libkafka in xero-core and xero-chain, libpostal in xero-lambda-text-address.
.PHONY: golang_build_golang
golang_build_golang:
	@echo "* PREPARE AS BUILDER: '"$(IMAGE)"'"
	@touch $(IMAGE)
	@docker build -t $(IMAGE) .
	@rm -f $(IMAGE)
	@echo "* BUILD: '"$(IMAGE)"'"
	docker run --rm -v $(SOURCE):$(SOURCE) -v $(HOME):/root -w $(PWD) -e GOPATH=$(GOPATH) -e GO111MODULE=on $(IMAGE) go build -v -o $(IMAGE)
	@echo "* DONE : make golang_build"

# Run go test
.PHONY: golang_test
golang_test:
	docker run --rm -v $(SOURCE):$(SOURCE) -v $(HOME):/root -w $(PWD) -e GOPATH=$(GOPATH) -e GO111MODULE=on $(GOLANG) go test

# build the given container
.PHONY: docker_build
docker_build: Dockerfile
	docker build --build-arg NODE_ENV=$(NODE_ENV) --build-arg ENGINE=$(ENGINE) -t $(IMAGE) .
	@echo "* DONE : make docker_build"
	@echo "* NEXT : to publish, execute 'make publish'"

# publish the given container 
.PHONY: docker_publish
docker_publish:
	docker tag $(IMAGE) $(TAG)
ifeq ($(PLATFORM),aws)
# e.g., aws ecr describe-repositories --region us-east-1 --repository-name "xero-text-address" 2>/dev/null
ifeq ($(shell aws ecr describe-repositories --region $(AWS_REGION) --repository-names "$(IMAGE)" >/dev/null),)
	-aws ecr create-repository --region $(AWS_REGION) --repository-name "$(IMAGE)"
endif
    # @exec $(shell aws ecr get-login --region $(AWS_REGION) --no-include-email --password-stdin)
	docker push $(TAG)
endif
ifeq ($(PLATFORM),gcloud)
	docker push $(TAG)
	@# gcloud v.18.03 doesnt support direct docker push, 
	@# use the following command instead
	@# gcloud docker -- push $(TAG)
endif
	@echo "* DONE : make docker_publish"

# create an ingress if one exists
.PHONY: kube_ingress
kube_ingress:
ifneq ($(shell find . -name "kube_ingress.yaml"),)
	kubectl -n $(NAMESPACE) apply -f kube_ingress.yaml
	@echo "* DONE : make kube_ingress"
endif

# delete the ingress if one exists
.PHONY: kube_uningress
kube_uningress:
ifneq ($(shell find . -name "kube_ingress.yaml"),)
	kubectl -n $(NAMESPACE) delete -f kube_ingress.yaml
	@echo "* DONE : make kube_uningress"
endif

# create the configmap
.PHONY: kube_configmap
kube_configmap:
ifneq ($(shell find . -name "kube_configmap.yaml"),)
	kubectl -n $(NAMESPACE) apply -f kube_configmap.yaml
	@echo "* DONE : make kube_configmap"
endif

# delete the configmap
.PHONY: kube_unconfigmap
kube_unconfigmap:
ifneq ($(shell find . -name "kube_configmap.yaml"),)
	kubectl -n $(NAMESPACE) delete -f kube_configmap.yaml
	@echo "* DONE : make kube_unservice"
endif

# create the service
.PHONY: kube_service
kube_service:
ifneq ($(shell find . -name "kube_service.yaml"),)
	kubectl -n $(NAMESPACE) apply -f kube_service.yaml
	@echo "* DONE : make kube_service"
endif

# delete the service
.PHONY: kube_unservice
kube_unservice:
ifneq ($(shell find . -name "kube_service.yaml"),)
	kubectl -n $(NAMESPACE) delete -f kube_service.yaml
	@echo "* DONE : make kube_unservice"
endif

# scale deployment to zero, 
# note this depends on our naming convention, $(IMAGE)-deployment
.PHONY: kube_unscale
kube_unscale:
	-kubectl -n $(NAMESPACE) scale --replicas=0 deployment $(IMAGE)-deployment

# create the deployment
.PHONY: kube_deployment
kube_deployment:
ifneq ($(shell find . -name "kube_deployment.yaml"),)
	@mkdir -p .tmp
	@export TAG=$(TAG) REGISTRY=$(REGISTRY) REPLICAS=$(REPLICAS) DATA_CONNECTION_URI=$(DATA_CONNECTION_URI) AWS_BUCKET=$(AWS_BUCKET) AWS_REGION=$(AWS_REGION) KAFKA_CHAIN_HOSTS=$(KAFKA_CHAIN_HOSTS) MOUNTPOINT=$(MOUNTPOINT) VERSION=$(VERSION); j2 kube_deployment.yaml > .tmp/kube_deployment.yaml
	kubectl -n $(NAMESPACE) apply -f .tmp/kube_deployment.yaml
	@echo "* DONE : make kube_deployment"
endif

# delete the deployment
.PHONY: kube_undeployment
kube_undeployment:
ifneq ($(shell find . -name "kube_deployment.yaml"),)
	@mkdir -p .tmp
	@export TAG=$(TAG) REGISTRY=$(REGISTRY) REPLICAS=$(REPLICAS) DATA_CONNECTION_URI=$(DATA_CONNECTION_URI) AWS_BUCKET=$(AWS_BUCKET) AWS_REGION=$(AWS_REGION) KAFKA_CHAIN_HOSTS=$(KAFKA_CHAIN_HOSTS) MOUNTPOINT=$(MOUNTPOINT) VERSION=$(VERSION); j2 kube_deployment.yaml > .tmp/kube_deployment.yaml
	kubectl -n $(NAMESPACE) delete -f .tmp/kube_deployment.yaml
	@echo "* DONE : make kube_undeployment"
endif

# list the deployment status
.PHONY: kube_status
kube_status:
	@#kubectl config get-contexts $(shell kubectl config current-context)
	kubectl -n $(NAMESPACE) get all

# default build
.PHONY: build
build:
	@echo "* ERROR: 'build' does not have a default rule, use 'make' instead"

# default publish
.PHONY: publish-default
publish-default: docker_publish
	@echo "* NEXT : to deploy, execute 'make (re)deploy'"

# default deploy
.PHONY: deploy-default
deploy-default: kube_configmap kube_deployment kube_service
	@echo "* NEXT : to check status, execute 'make status'"

# default apply (e.g., after change)
.PHONY: apply-default
apply-default: kube_deployment_apply
	@echo "* NEXT : to check status, execute 'make status'"

# default undeploy
.PHONY: undeploy-default
undeploy-default: kube_unservice kube_undeployment kube_unconfigmap
	@echo "* NEXT : to check status, execute 'make status'"

# default redeploy
.PHONY: redeploy-default
redeploy-default: kube_unscale kube_configmap kube_deployment kube_service
	@echo "* NEXT : to check status, execute 'make status'"

# default test
.PHONY: test-default
test-default:
	docker run --rm -v $(SOURCE):$(SOURCE) -v $(HOME):/root -w $(PWD) -e GOPATH=$(GOPATH) -e GO111MODULE=on $(GOLANG) go test $(TESTPKGS)
	@echo "* NEXT : to check status, execute 'make status'"

# default status
.PHONY: status-default
status-default: kube_status

%: %-default
	@ true
