# [TBW]ファイルコンバータ

## 使い方
```
python src/main.py [入力ファイル] [出力ファイル] [オプション(複数指定可)]
```

## 実行例
[TBW]

## オプションについて
[TBW]

## 開発準備
Pipfileにしたがってライブラリ等をインストールします
```
pipenv install
pipenv shell
```

## コードチェッカー
規約に違反している箇所を明示します
```
pipenv run lint
```
反している規約と改善案を明示します
```
pipenv run format-check
```
明示された改善案通りに修正します  
※意図しない変更が発生しうるので必ずformat-check後に実施してください
```
pipenv run format
```

## テストの実行
```
pipenv run pytest
```

## ライブラリの追加と削除
```
pipenv install [hoge]
pipenv uninstall [hoge]
```

## CI/CD
[TBW]  
.gitlab_ci  
で設定可能です  
