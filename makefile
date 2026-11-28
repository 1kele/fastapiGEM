
# ===============================
# Настройки проекта
# ===============================
PY_SRCS := src
RADON_MIN_MI := 50

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: help install lint lint-fix fmt fmt-check type security cc mi hal raw check fix

# ===============================
# Помощь
# ===============================
help:
	@echo "Доступные команды:"
	@echo "make install    - установить зависимости"
	@echo "make lint       - проверить Ruff"
	@echo "make lint-fix   - автоматически исправить Ruff"
	@echo "make fmt        - отформатировать код"
	@echo "make fmt-check  - проверить форматирование"
	@echo "make type       - проверить типы Mypy"
	@echo "make security   - проверить безопасность Bandit"
	@echo "make cc         - цикломатическая сложность"
	@echo "make mi         - индекс поддерживаемости"
	@echo "make hal        - метрики Холстеда"
	@echo "make raw        - статистика кода"
	@echo "make check      - запустить все проверки"
	@echo "make fix        - исправить стиль и форматирование"

# ===============================
# Зависимости
# ===============================
install:
	uv sync

# ===============================
# Ruff
# ===============================
lint:
	uv run ruff check $(PY_SRCS)

lint-fix:
	uv run ruff check $(PY_SRCS) --fix

fmt:
	uv run ruff format $(PY_SRCS)

fmt-check:
	uv run ruff format --check $(PY_SRCS)

# ===============================
# Mypy
# ===============================
type:
	uv run mypy $(PY_SRCS)

# ===============================
# Bandit
# ===============================
security:
	uv run bandit -r $(PY_SRCS) -lll -x .venv,venv,build,dist,migrations

# ===============================
# Radon: цикломатическая сложность
# ===============================
cc:
	uv run radon cc -s -a $(PY_SRCS)
	@if uv run radon cc -s $(PY_SRCS) | grep -E '\- [EF] '; then \
		echo "ERROR: обнаружена сложность E/F"; \
		exit 1; \
	else \
		echo "OK: сложность E/F не обнаружена"; \
	fi

# ===============================
# Radon: индекс поддерживаемости
# ===============================
mi:
	uv run radon mi -s $(PY_SRCS)
	@uv run radon mi -s $(PY_SRCS) | awk -v min="$(RADON_MIN_MI)" '\
		match($$0, /\([0-9.]+\)/) { \
			score = substr($$0, RSTART + 1, RLENGTH - 2); \
			if (score + 0 < min) { \
				print "ERROR: MI ниже порога:", $$0; \
				bad = 1; \
			} \
		} \
		END { exit bad }'
	@echo "OK: Maintainability Index >= $(RADON_MIN_MI)"

# ===============================
# Radon: метрики Холстеда
# ===============================
hal:
	uv run radon hal $(PY_SRCS)

# ===============================
# Radon: статистика кода
# ===============================
raw:
	uv run radon raw $(PY_SRCS)

# ===============================
# Автоматическое исправление
# ===============================
fix: lint-fix fmt

# ===============================
# Полная проверка проекта
# ===============================
check: lint fmt-check type security cc mi hal raw
	@echo "Все проверки завершены успешно"
