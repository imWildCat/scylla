default:
	make gen-rst
	make build-assets
	make build-package
	make upload
build-package:
	rm -rf dist
	python setup.py bdist_wheel --universal
upload:
	twine upload dist/*
tag:
	git tag $(TAG) -m '$(MSG)' && git push --tags origin master
delete-tag:
	git tag --delete $(TAG); git push --delete origin $(TAG)
gen-rst:
	pandoc -s README.md -o README.rst
build-assets:
	parcel build --public-url='/assets' -d scylla/assets frontend/src/index.html
assets-dev:
	parcel --public-url='/assets' frontend/src/index.html