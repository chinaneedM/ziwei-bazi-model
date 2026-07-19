.PHONY: test verify

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

verify:
	PYTHONPATH=src python -m fortune_training.cli verify
