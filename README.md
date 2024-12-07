# Tech Blog Agents

AIエージェントを活用した技術ブログ記事生成システム

## 概要

このプロジェクトは、複数のAIエージェントを組み合わせて技術ブログ記事を生成するPythonアプリケーションです。ユーザーが提供する断片的な情報から、構造化された技術ブログ記事を生成し、フィードバックを反映して記事を改善することができます。

## 特徴

- 複数のAIエージェントによる段階的な記事生成
- ユーザーフィードバックに基づく記事の改善
- Markdown形式での出力
- YAMLフロントマターによるメタデータ管理
- 4000文字程度の技術記事を生成

## システム構成

### エージェント

- **Draft Agent**: 初稿の生成
- **Style Agent**: 文章スタイルの改善
- **Technical Agent**: 技術的な正確性の確認
- **Revision Agent**: フィードバックに基づく修正

### 入出力

- 入力: `input/fragments/`ディレクトリ内のMarkdownファイル
- 出力: 
  - 記事: `output/blogs/`ディレクトリ
  - 下書き: `output/drafts/`ディレクトリ

## セットアップ

1. 必要なツール
   - Python 3.11以上
   - Poetry

2. インストール
```bash
# 環境のセットアップ
make init
make install

# または
poetry install
```

3. 環境変数の設定
```bash
# .envファイルを作成
cp .env.example .env

# APIキーとモデルを設定
OPENAI_API_KEY=your-api-key-here
MODEL_NAME=gpt-4-turbo-preview
```

## 使用方法

1. 入力ファイルの作成
```markdown
# input/fragments/your-article.md
---
title: 記事のタイトル
tags:
  - タグ1
  - タグ2
---

# キーポイント
- ポイント1
- ポイント2

# 補足情報
- 補足1
- 補足2
```

2. 記事の生成
```bash
# デフォルトの入力ファイルで実行
make run

# 特定のファイルを指定して実行
make run INPUT_FILE=your-article.md

# フィードバックなしで実行
make run-no-feedback
```

3. フィードバックの提供
- 生成された下書きを確認
- フィードバックファイル（.feedback.md）を編集
- 満足するまで繰り返し

## 開発用コマンド

```bash
# コードフォーマット
make format

# リンター実行
make lint

# テスト実行
make test

# キャッシュクリア
make clean

# 全処理の実行
make all
```

## ディレクトリ構造

```
project-root/
├─ src/
│  ├─ agents/        # AIエージェントの実装
│  ├─ config/        # 設定ファイル
│  ├─ graph/         # ワークフロー制御
│  └─ utils/         # ユーティリティ関数
├─ tests/            # テストコード
├─ input/            # 入力ファイル
│  └─ fragments/
└─ output/           # 出力ファイル
   ├─ blogs/         # 生成された記事
   └─ drafts/        # 下書きとフィードバック
```
