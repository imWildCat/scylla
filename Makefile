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
	NODE_ENV=production node_modules/.bin/parcel build --public-url='/assets' -d scylla/assets frontend/src/index.html
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
install-dependencies-ubuntu:
	sudo apt-get update -y
	sudo apt-get install libgnutls28-dev libcurl4-openssl-dev libssl-dev -y
	# sudo apt-get install -y libgbm-dev gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
