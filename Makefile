PYTHON ?= python

.PHONY: setup test demo api web web-build

setup:
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m pytest -q

demo:
	sentinelcare-demo

api:
	sentinelcare-api

web:
	cd frontend/web && npm install && npm run dev

web-build:
	cd frontend/web && npm ci && npm run build

