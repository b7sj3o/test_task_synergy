# Use bash for better compatibility (Git Bash on Windows is supported)
SHELL := /usr/bin/env bash

# -------- Variables --------
VENV_DIR := backend/.venv
PYTHON   := python

# Try to activate POSIX or Windows venv
define ACTIVATE
. $(VENV_DIR)/Scripts/activate
endef

.PHONY: help install install-backend install-frontend \
	dev dev-backend dev-frontend \
	build build-backend build-frontend preview-frontend \
	lint lint-backend lint-frontend \
	test test-backend \
	clean clean-venv

help:
	@echo "Available targets:"
	@echo "  make install            Install backend and frontend deps"
	@echo "  make dev                Run backend and frontend dev servers"
	@echo "  make dev-backend        Run FastAPI (uvicorn) dev server"
	@echo "  make dev-frontend       Run Vite dev server"
	@echo "  make build              Build frontend (and any backend if needed)"
	@echo "  make preview-frontend   Preview built frontend"
	@echo "  make lint               Run linters (best-effort)"
	@echo "  make test               Run backend tests (pytest)"
	@echo "  make clean              Clean build/test artifacts"
	@echo "  make clean-venv         Remove backend virtualenv"

# -------- Install --------
install: install-backend install-frontend

install-backend:
	$(PYTHON) -m venv $(VENV_DIR)
	($(ACTIVATE); pip install -U pip; pip install -r backend/requirements.txt)

install-frontend:
	cd frontend && (npm ci || npm install)

# -------- Development --------
dev:
	$(MAKE) dev-backend & \
	$(MAKE) dev-frontend & \
	wait

dev-backend:
	($(ACTIVATE); uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend)

dev-frontend:
	cd frontend && npm run dev -- --host 0.0.0.0 --port 5173

# -------- Build / Preview --------
build: build-backend build-frontend

build-backend:
	@echo "No backend build step. Using live sources."

build-frontend:
	cd frontend && npm run build

preview-frontend:
	cd frontend && npm run preview

# -------- Lint / Test --------
lint: lint-backend lint-frontend

lint-backend:
	-($(ACTIVATE); ruff check)
	-($(ACTIVATE); flake8)

lint-frontend:
	cd frontend && npm run lint || true

test: test-backend

test-backend:
	($(ACTIVATE); pytest -q)

# -------- Clean --------
clean:
	rm -rf frontend/dist
	rm -rf backend/.pytest_cache
	find backend -type d -name "__pycache__" -exec rm -rf {} +
	find backend -type d -name ".mypy_cache" -exec rm -rf {} +

clean-venv:
	rm -rf $(VENV_DIR)


