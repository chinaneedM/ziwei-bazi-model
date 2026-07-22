.PHONY: test verify knowledge-verify

test:
	PYTHONPATH=src:$${PYTHONPATH} python -m unittest discover -s tests -v

verify:
	PYTHONPATH=src:$${PYTHONPATH} python -m fortune_training.cli verify
	python tools/build_knowledge_batch_a.py --check
	python tools/validate_knowledge_workbench.py

knowledge-verify:
	python tools/build_knowledge_batch_a.py --check
	python tools/validate_knowledge_workbench.py
