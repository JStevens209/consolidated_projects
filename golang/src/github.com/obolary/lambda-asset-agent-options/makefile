IMAGE = lambda-asset-agent-options
VERSION = $(shell git describe --abbrev=0 --tags)
NAMESPACE = obolary

ENGINE = deterministic.mock

REPLICAS ?= 1

default: docker_build

include ../core/base.make
