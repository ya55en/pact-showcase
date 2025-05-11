FRONTEND_APPNAME := TodoApiClient
FRONTEND_DIR := frontend
CLIENT_SRC := $(FRONTEND_DIR)/src
CLIENT_TESTS := $(FRONTEND_DIR)/test
PACTS_DIR := $(FRONTEND_DIR)/pacts

CLIENT_SOURCES := $(shell find $(CLIENT_SRC) -type f -name '*.js')
CLIENT_PACT_TESTS := $(shell find $(CLIENT_TESTS)/pact -type f -name '*.spec.js')

BACKEND_APPNAME := TodoBackend

PACT_FILE_PATH := $(PACTS_DIR)/$(FRONTEND_APPNAME)-$(BACKEND_APPNAME).json


$(PACT_FILE_PATH):  $(CLIENT_SOURCES) $(CLIENT_PACT_TESTS)
	cd $(FRONTEND_DIR) && npm run pact


pact-publish:  $(PACT_FILE_PATH)
	COMMIT_HASH=$(shell git log --grep='(fe)' -1 --format=%h) ; \
		pact-broker publish --consumer-app-version=$$COMMIT_HASH $(PACT_FILE_PATH)


.PHONY: pact-publish
