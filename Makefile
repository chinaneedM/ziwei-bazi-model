.PHONY: test audit install-check package

test:
	python3 -m unittest discover -s tests -v

audit:
	PYTHONPATH=src python3 -m fortune_v1.cli audit-sources --source-dir ../project_sources --config config/runtime.json --output reports/source-audit.json

install-check:
	PYTHONPATH=src python3 -m fortune_v1.cli install-check --repo-root . --source-audit reports/source-audit.json --test-report reports/test-report.json --topology-receipt config/current-topology-receipt.json --output reports/install-receipt.json

package:
	git archive --format=zip --output=../fortune-v1-source.zip HEAD

