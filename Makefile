SHELL=/bin/bash

TEST_ENV=( [[ "$$CONDA_PREFIX" == */FinBrain ]] || \
		 (echo -e "\nERROR: environment not active: run '. ./activate'" && false) )

REQ=requirements/requirements
REQS=$(REQ).txt \
	$(REQ).deploy.txt \
	$(REQ).dev.txt

PY=python
PIPC=pip-compile

NEW_SHELL=$(shell getent passwd $$USER | awk -F: '{print $$NF}')

# tools profile
PROFILE=client

.PHONY: create-env
create-env:
	conda create -n FinBrain -y python=3.10
	@echo "Run: '. ./activate' to finish setup"

# Atualizar pip para a versão mais recente
.PHONY: update-pip
update-pip:
	$(PY) -m pip install --upgrade pip

# install dependencies
.PHONY: install-deps-docker
install-deps-docker: update-pip compile-deps
	@$(TEST_ENV)
	$(PY) -m pip install -U \
		-r $(REQ).txt \
		-r $(REQ).dev.txt \
		-r $(REQ).deploy.txt

# install dependencies
.PHONY: install-deps
install-deps: update-pip compile-deps
	$(PY) -m pip install -U \
		-r $(REQ).txt \
		-r $(REQ).dev.txt \
		-r $(REQ).deploy.txt

# compile (lock) dependencies
.PHONY: compile-deps
compile-deps: $(REQS)

# compile (lock) dependencies
.PHONY: compile-deps-clean
compile-deps-clean:
	rm -f $(REQS)

# # compile requirements
# $(REQS): %.txt : %.in
# 	@$(TEST_ENV)
# 	@rm -rf $@
# 	$(PIPC) -U -q $<

# build docker image
build:
	docker build -t crdtanqa001.azurecr.io/pricing .

run_docker:
	docker run --rm -it  --platform linux/amd64 -v ${PWD}/config.local.env:/app/config.local.env:ro crdtanqa001.azurecr.io/pricing:461 /app/run task pricing.pipeline:run -d $(date +%Y%M%d)