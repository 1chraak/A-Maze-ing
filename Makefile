PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean lint

install:
	$(PYTHON) -m pip install --break-system-packages flake8 mypy

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -name "*.pyc" -delete
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -f maze.txt

lint:
	flake8 *.py
	mypy *.py --warn-return-any --warn-unused-ignores --ignore-missing-imports
