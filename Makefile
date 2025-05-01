.PHONY: setup vendor dev deploy test lint format

# Default target
all: setup vendor

# Setup Python environment
setup:
	@echo "Setting up Python environment..."
	uv venv .venv
	. .venv/bin/activate && uv pip install pyodide-build
	pyodide venv .venv-pyodide

# Install vendored packages
vendor:
	@echo "Installing vendored packages..."
	.venv-pyodide/bin/pip install -t src/vendor -r vendor.txt

# Install test dependencies
test-setup:
	@echo "Installing test dependencies..."
	. .venv/bin/activate && uv pip install -r requirements-test.txt

# Run development server
dev:
	@echo "Starting development server..."
	npx wrangler@latest dev

# Deploy to Cloudflare Workers
deploy:
	@echo "Deploying to Cloudflare Workers..."
	npx wrangler@latest deploy

# Run tests
test: test-setup
	@echo "Running tests..."
	. .venv/bin/activate && pytest tests

# Run linting
lint:
	@echo "Running linter..."
	. .venv/bin/activate && ruff check .

# Format code
format:
	@echo "Formatting code..."
	. .venv/bin/activate && ruff format .

# Clean up generated files
clean:
	@echo "Cleaning up..."
	rm -rf .venv .venv-pyodide
	find . -type d -name "__pycache__" -exec rm -rf {} +
