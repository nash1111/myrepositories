## devcontainerを使わない場合
testという名前でdocker imageをビルドします、Dockerfileと同じ階層にいる場合は下記のコマンド  
違う階層にいるDockerfileを読む場合は```.```をパスに変更します

```
docker build -t test .
```

## コンテナ内にログイン
```
docker run -it test bash
```

## コンテナ外からコマンド実行
バックグラウンドで走らせる
```
docker run -d test
```

```
docker exec -it [CONTAINER_ID] python3 sample.py
```

## Docker利用においてVSCodeの必要性
TBW
devcontainer機能, Dockerfileのチェック機能, vscode-extensionの持ち込みと統一


## コンテナ内にファイルをコピー
### 基本的にscpと似たコマンドです, CONTAINER IDを指定する必要があります
dockerを走らせた状態にしておきます
docker psで、目的のコンテナIDを確認します
```
docker ps
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS          PORTS                NAMES
3bf4a7188d39   docker101tutorial   "/docker-entrypoint.…"   55 minutes ago   Up 55 minutes   0.0.0.0:80->80/tcp   docker-tutorial
```

```
docker cp [ローカルファイルのpath] [CONTAINER ID]:path
```

## コンテナ外にファイルをコピー
```
docker cp [CONTAINER ID]:path [コピーを配置したいローカルのpath]
```

## 定期的に確認
不要なimageが蓄積する場合があるので下記のコマンドで確認、不要なものは消去してください
```
docker system df
```
一括消去
```
docker system prune -a --volumes
```