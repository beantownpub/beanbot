.PHONY: all test clean

name := $(subst _,-,$(@D))
image := beanbot
# tag := $(shell grep 'appVersion:' $(@D)/Chart.yaml | cut -f 2 -d' ')
port := 5007

SHELL := /bin/bash

ifeq ($(env),dev)
	context = ${DEV_CONTEXT}
	namespace = ${DEV_NAMESPACE}
	log_level ?= DEBUG
else ifeq ($(env),prod)
	context = ${PROD_CONTEXT}
	namespace = ${PROD_NAMESPACE}
	log_level ?= INFO
endif

helm/clean:
		rm helm/beanbot/*.tgz || true

helm/context:
	kubectl config use-context $(context)

## Publish contact Helm chart
helm/publish:
	cd helm/beanbot && helm package . && \
		cd - && \
		helm repo index . --url https://beantownpub.github.io/helm/ && \
		git add beanbot/

## Deploy beanbot to cluster
helm/install: helm/context
	cd helm/beanbot && \
	helm upgrade --install beanbot . \
		--namespace $(namespace) \
		--set global.env=$(env) \
		--set logLevel=$(log_level) \
		--debug
	@echo $(name)

## Render beanbot templates
helm/template:
	helm template  beanbot helm/beanbot/ \
		--namespace $(namespace) \
		--set global.env=$(env) \
		--set logLevel=$(log_level) \
		--debug

helm/port_forward: helm/context
		kubectl port-forward --namespace $(namespace) svc/beanbot $(port):$(port)
