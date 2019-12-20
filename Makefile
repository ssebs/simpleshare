all:
	@echo "Building Simpleshare..."
	( \
		source ./venv/bin/activate; \
		pyinstaller simpleshare/__main__.py --clean -F -n simpleshare --icon=simpleshare/img/simpleshare_logo.ico; \
	)
	@echo "Built files are in ./dist/"
publish:
	@rm -rf ./dist/*
	@python3.8 setup.py sdist bdist_wheel
	@python3.8 -m twine upload --repository-url https://upload.pypi.org/legacy/ ./dist/* --verbose
