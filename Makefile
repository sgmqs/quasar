TEST_PATH=./

.PHONY: clean

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

test: clean
	python -m unittest
	# py.test --verbose --color=yes $(TEST_PATH)