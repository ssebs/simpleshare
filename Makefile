all:
	@echo "Building Simpleshare..."
	( \
		source ./venv/bin/activate; \
		pyinstaller simpleshare/__main__.py --clean -F -n simpleshare; \
	)
	@echo "Built files are in ./dist/"
