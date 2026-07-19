PYTHON ?= python3
REPOSITORY_VISIBILITY ?= public
EXPECTED_COMMIT ?= $(shell git rev-parse HEAD)
ACTIVATION_MODE ?= candidate
INSTALL_RECEIPT ?= reports/final-open-source-install-receipt-v3.json

.PHONY: test source-import audit install-check package

test:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) -m pytest -q

audit:
	PYTHONPATH=src $(PYTHON) -m fortune_v1.cli audit-sources --source-dir knowledge/base --config config/runtime.json --output reports/source-audit.json

source-import:
	PYTHONPATH=src $(PYTHON) -m fortune_v1.cli import-source-package --package "$(PACKAGE)" --expected-zip-sha256 "$(PACKAGE_SHA256)" --config config/runtime.json --work-root .source-import-work --reports-dir reports --migrate-destination knowledge/base

install-check:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) -m pytest -q
	FORTUNE_INSTALL_TESTS_PASSED=1 PYTHONPATH=src $(PYTHON) scripts/final-open-source-install-check.py \
		--root . \
		--visibility "$(REPOSITORY_VISIBILITY)" \
		--expected-commit "$(EXPECTED_COMMIT)" \
		--activation-mode "$(ACTIVATION_MODE)" \
		--output "$(INSTALL_RECEIPT)"

package:
	git archive --format=zip --output=../fortune-v1-source.zip HEAD
