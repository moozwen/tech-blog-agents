.PHONY: install format lint test run clean

# デフォルトの入力ファイル
INPUT_FILE ?= ai-agent-development.md
FEEDBACK_OPT ?=

install:
	poetry install

format:
	poetry run black src tests
	poetry run isort src tests

lint:
	poetry run flake8 src tests

test:
	poetry run pytest

# 入力ファイルを引数として受け取る
run:
	poetry run python -m src.main $(INPUT_FILE) $(FEEDBACK_OPT)

# フィードバックなしで実行
run-no-feedback:
	poetry run python -m src.main $(INPUT_FILE) --no-feedback

# 特定の入力ファイルで実行する例
run-ai-agent:
	poetry run python -m src.main ai-agent-development.md $(FEEDBACK_OPT)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -rf output/drafts/*
	rm -rf output/blogs/*

# 必要なディレクトリを作成
init:
	mkdir -p input/fragments
	mkdir -p output/blogs
	mkdir -p output/drafts

# 全体の処理を実行（フォーマット、リント、テスト、実行）
all: format lint test run