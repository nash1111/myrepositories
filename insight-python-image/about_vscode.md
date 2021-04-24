1つのDocker環境に対して毎回build, run, bashするのは現実的でないので次の拡張機能をVSCodeにインストールします
https://github.com/microsoft/vscode-dev-containers

VSCodeを開いた状態で```Ctrl+Shift+X```を押して、検索欄にremote-containerと入力してください  

### Remote Containerの機能
- 作業環境をDockerで完結させる
- vscode拡張機能の管理


### Remote Containerの使い方
remote-containerをインストールした状態でプロジェクトを開くと
```
Folder contains a Dev Container configuration file. Reopen folder to develop in a container (learn more).
Don't Show Again | Reopen in Container
```
と表示されるのでReopen in Containerをクリックします  
表示されない場合はVSCode左下をクリックします    
VSCodeが.devcontainerの設定ファイルを読み込み記述通りのDocker環境をビルドしてログインまで行ってくれます  
正常に実行されると左下の表示が緑色に変わり  
```Dev Container: [docker image 名]```となります  
Docker環境を抜けたい場合左下をクリック>