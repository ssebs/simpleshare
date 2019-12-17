all:
	@echo "You must define a specific target. (cli, gui)"
cli:
	@echo "Building CLI..."
	( \
		source ./venv/bin/activate; \
		pyinstaller simpleshare.py --clean -F -n simpleshare-cli; \
	)
	@echo "Built files are in ./dist/"
gui:
	@echo "Building GUI..."
