.PHONY: test source-import audit install-check package

test:
	python3 -m unittest discover -s tests -v

audit:
	PYTHONPATH=src python3 -m fortune_v1.cli audit-sources --source-dir knowledge/base --config config/runtime.json --output reports/source-audit.json

source-import:
	PYTHONPATH=src python3 -m fortune_v1.cli import-source-package --package "$(PACKAGE)" --expected-zip-sha256 "$(PACKAGE_SHA256)" --config config/runtime.json --work-root .source-import-work --reports-dir reports --migrate-destination knowledge/base

install-check:
	PYTHONPATH=src python3 -m fortune_v1.cli install-check --repo-root . --source-audit reports/source-audit.json --binding-receipt reports/binding-table-recompute-receipt.json --migration-receipt reports/migration-receipt.json --prompt-snapshot reports/prompt-snapshot-status.json --test-report reports/test-report.json --topology-receipt config/current-topology-receipt.json --answer-workflow-receipt reports/answer-vault-workflow-readback.json --external-runner config/external-runner.json --output reports/install-receipt.json

package:
	git archive --format=zip --output=../fortune-v1-source.zip HEAD
