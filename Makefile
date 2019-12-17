all:
	@echo "Building Simpleshare..."
	( \
		source ./venv/bin/activate; \
		pyinstaller simpleshare.py --clean -F -n simpleshare-cli; \
	)
	@echo "Built files are in ./dist/"
