# Pytest diagnostic

Exit status: 2

```text

==================================== ERRORS ====================================
__________ ERROR collecting tests/test_public_envelope_end_to_end.py ___________
ImportError while importing test module '/home/runner/work/ziwei-bazi-model/ziwei-bazi-model/tests/test_public_envelope_end_to_end.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_public_envelope_end_to_end.py:9: in <module>
    import tests.test_end_to_end_pipeline as e2e_fixture
E   ModuleNotFoundError: No module named 'tests'
=========================== short test summary info ============================
ERROR tests/test_public_envelope_end_to_end.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```
