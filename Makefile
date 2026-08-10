.PHONY: test verify canonical-runtime canonical-source-access canonical-source-access-validate

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

verify:
	PYTHONPATH=src python -m fortune_training.cli verify

canonical-runtime:
	PYTHONPATH=src python -m fortune_training.cli canonical-runtime-build

canonical-source-access:
	PYTHONPATH=src python -m fortune_training.cli canonical-source-access-build

canonical-source-access-validate:
	PYTHONPATH=src python -m fortune_training.cli canonical-source-access-validate
