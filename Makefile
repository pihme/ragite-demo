PYTHON ?= python3
# Path to libragite.so: the pinned release that build-demo-db downloads, unless you pass your own.
RAGITE_LIB ?= ./libragite.so
PORT ?= 8001

.PHONY: demo-db test serve smoke screenshots clean

demo-db: ## Download the pinned sources and build app/demo.db
	$(PYTHON) scripts/build-demo-db $(if $(LIB),--lib $(LIB))

test: ## Datasette test-client checks against app/demo.db
	RAGITE_LIB=$(if $(LIB),$(LIB),$(RAGITE_LIB)) $(PYTHON) -m pytest -q

serve: ## Serve the demo with the search page on http://127.0.0.1:$(PORT)/search
	datasette serve app --load-extension $(basename $(if $(LIB),$(LIB),$(RAGITE_LIB))) --port $(PORT)

smoke: ## Query a running `make serve` over HTTP
	scripts/smoke http://127.0.0.1:$(PORT)

clean:
	rm -f app/demo.db app/demo.db.part
