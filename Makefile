TEST_PATH=./

.PHONY: clean

build:
	pip install --upgrade .
	
clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

clean-build:
	find . -name '*.egg*' -exec rm -rf --force {} +

test: clean
	python -m unittest
	# py.test --verbose --color=yes $(TEST_PATH)