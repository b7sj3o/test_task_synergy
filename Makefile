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
	($(ACTIVATE); uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 --app-dir backend)

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


