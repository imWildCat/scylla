default:
	make assets-build
	make package-build
	make upload
package-build:
	rm -rf dist
	python setup.py bdist_wheel --universal
upload:
	twine upload dist/*
tag:
	git tag $(TAG) -m '$(MSG)' && git push --tags origin master
delete-tag:
	git tag --delete $(TAG); git push --delete origin $(TAG)
assets-build:
	make assets-clean
	cd frontend && NODE_ENV=production npm run build
assets-dev:
	node_modules/.bin/parcel --public-url='/assets' frontend/src/index.html
assets-clean:
	rm -rf scylla/assets
	rm -rf build/lib/scylla/assets
	rm -rf dist/scylla/scylla/assets
doc:
	make doc-en
	make doc-zh
doc-en:
	cd docs/source && sphinx-apidoc -f -o . ../../scylla
	cd docs && PYTHONPATH=../ make html
doc-zh:
	cd docs_zh/source && sphinx-apidoc -f -o . ../../scylla
	cd docs_zh && PYTHONPATH=../ make html
style-check:
	flake8 . --count --config=.flake8.cfg --select=E901,E999,F821,F822,F823 --show-source --statistics
test:
	make style-check
	pytest --cov=./scylla tests
