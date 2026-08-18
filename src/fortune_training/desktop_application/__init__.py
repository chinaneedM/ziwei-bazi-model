"""Windows portable desktop distribution for the Combined Chart Workbench.

Keep package initialization side-effect free. Build helpers are executed with
``python -m fortune_training.desktop_application.distribution``; eager imports
here would pre-import that module before ``runpy`` executes it.
"""
