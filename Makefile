.PHONY: test verify canonical-runtime

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

verify:
	PYTHONPATH=src python -m fortune_training.cli verify

canonical-runtime:
	PYTHONPATH=src python -m fortune_training.cli canonical-runtime-build
