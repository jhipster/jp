---
layout: default
title: アプリケーションのアップグレード
permalink: /upgrading-an-application/
sitemap:
    priority: 0.7
    lastmod: 2024-04-08T00:00:00-00:00
gitgraph: http://jsfiddle.net/lordlothar99/tqp9gyu3
---

# <i class="fa fa-refresh"></i> アプリケーションのアップグレード

## サマリー

1. [選択1 - 自動アップグレード](#automatic_upgrade)
2. [選択2 - 手動アップグレード](#manual_upgrade)

<h2 id="automatic_upgrade">選択1 - 自動アップグレード</h2>

JHipsterの新しいバージョンがリリースされると、JHipsterアップグレードサブジェネレータは、変更を消去することなく、既存のアプリケーションを新しいバージョンにアップグレードするのを手助けします。

これは、以下の場合に役立ちます。

- 既存のアプリケーションに最新のJHipsterの機能を搭載させる
- 重要なバグ修正またはセキュリティ更新がある場合に変更を取得する
- コードベースに加えた変更を保持し、新しく生成されたコードとマージする

_アップグレードを行う前にこのページをよく読んで、アップグレードプロセスがどのように機能するかを理解してください_

### 要件

このサブジェネレータを動作させるには、[http://git-scm.com](http://git-scm.com/)から`git`をインストールする必要があります。

### アップグレードサブジェネレータの実行

アプリケーションのルートディレクトリに移動します。

`cd myapplication/`

アプリケーションをアップグレードするには、次のように入力します。

`npx jhipster upgrade`

渡すことができるオプションは以下のとおりです。

* `--verbose` - アップグレードプロセスの各ステップを詳細に記録します。
* `--target-version 6.6.0` - 最新リリースではなく、ターゲットバージョンのJHipsterにアップグレードします。プロジェクトが数個のバージョン分遅れている場合に便利です。
* `--target-blueprint-versions kotlin@1.4.0,vuejs@1.3.0` - 各Blueprintの最新リリースではなく、ターゲットのBlueprintのバージョンにアップグレードします。ただし、Blueprintのターゲットバージョンは、ターゲットのJHipsterバージョンと互換性がある必要があります。
* `--force` - 新しいJHipsterバージョンが利用できない場合でも、アップグレードサブジェネレータを実行します。
* `--skip-checks` - プロジェクトの再生成時のチェックを無効にします。
* `--skip-install` - アップグレードプロセス中の依存関係のインストールをスキップします。
* `--silent` - 生成プロセスの出力を非表示にします。

複数回アップグレードする場合は、最初に次のようにJHipsterツリーをアップグレードすることを検討できます。
	
    git checkout jhipster_upgrade
	git checkout --patch master .yo-rc.json
	git checkout --patch master .jhipster
	git commit -a
	git push --set-upstream origin jhipster_upgrade
	git checkout master

上記の手順を実行すると、jhipster_upgradeツリーが最新の変更内容でアップグレードされるため、JHipsterはアップグレード中にそのツリーを利用できます。たとえば、モデルを変更した場合などです。

### JHipster 7以前のバージョンからのアップグレード

[マイグレートブループリント](https://github.com/jhipster/generator-jhipster-migrate)は、アップグレードサブジェネレータの高度なバージョンです。JHipster 7アプリをアップグレードする必要がある場合は、マイグレートブループリントを使用することをお勧めします。たとえば、7.9.3のアプリがあるとします。

最新バージョンにアップグレードするには、`jhipster-migrate`を実行します。競合を解決し、コミットして、祝杯を上げましょう！

実際の例については、21-Points Healthプロジェクトの以下のプルリクエストを参照してください。

- [JHipster 7.9.4へのアップグレード](https://github.com/mraible/21-points/pull/248)
- [JHipster 8.2.1へのアップグレード](https://github.com/mraible/21-points/pull/249)

### アップグレードプロセスをグラフィカルに表示

以下にアップグレードプロセスの動作を図で示します（テキストによる説明については、次のセクションを参照してください）。

![GitGraph]({{ site.url }}/images/upgrade_gitgraph.png)

（イメージは[JSFiddle](http://jsfiddle.net/lordlothar99/tqp9gyu3/)より（[日本語バージョンはこちら](https://jsfiddle.net/hide212131/gsxmucap/10/)））

上のグラフでは正しく表示されていませんが、`jhipster_upgrade`ブランチはプロジェクトで孤立して作成されることに注意してください。

### アップグレードプロセスの段階的な説明

JHipsterアップグレードサブジェネレータによって処理される手順は以下のとおりです。

1. 新しいバージョンのJHipsterが利用可能かどうかをチェックします（`--force`を使用している場合は適用されません）。
2. アプリケーションがすでに`git`リポジトリとして初期化されているかどうかをチェックします。そうでない場合は、JHipsterがリポジトリを初期化し、現在のコードベースをmasterブランチにコミットします。
3. リポジトリにコミットされていないローカル変更がないことを確認します。コミットされていない変更が見つかった場合、プロセスは終了します。
4. `jhipster_upgrade`ブランチが存在するかどうかをチェックします。存在しない場合は、ブランチが作成されます。このステップの詳細については、「最初のアップグレードの具体的な手順」のセクションを参照してください。
5. `jhipster_upgrade`ブランチをチェックアウトします。
6. JHipsterを利用可能な最新バージョンにグローバルにアップグレードします。
7. 現在のプロジェクトフォルダをクリーンアップします。
8. `jhipster --force`コマンドを使用してアプリケーションを再生成します。
9. 生成されたコードを`jhipster_upgrade`ブランチにコミットします。
10. `npx jhipster_upgrade`コマンドが起動された元のブランチに`jhipster_upgrade`ブランチをマージして戻します。
11. ここで、マージ競合がある場合は、それを解決する必要があります。

おめでとうございます。アプリケーションが最新バージョンのJHipsterにアップグレードされました。

### 最初のアップグレードの具体的な手順

JHipsterアップグレードサブジェネレータの最初の実行では、すべての変更が消去されないようにするため、いくつかの追加手順が実行されます。

1. `jhipster_upgrade`ブランチが孤立して作成されます（親がありません）。
2. アプリケーション全体が生成されます（現在のJHipsterバージョンを使用）。
3. ブロック・マージ（訳注：[Oursマージストラテジでのマージのようです](https://github.com/jhipster/generator-jhipster/issues/3696#issuecomment-225164954)）コミットが`master`ブランチで行われます。`master`ブランチのコードベースは変更されません。これは、`master`のHEADが現在のJHipsterバージョンで最新であることをGitに記録するための実用的な方法です。

### アドバイス

- `jhipster_upgrade`ブランチでは何もコミットしないでください。このブランチはJHipsterアップグレードサブジェネレータ専用です。サブジェネレータが実行されるたびに、新しいコミットが作成されます。

- 非常に古いバージョン（5.0.0から最新など）からアップデートする場合は、各マイナー/パッチバージョンの間に徐々にアップデートし、アプリケーションが期待どおりに動作することを確認するためのテストを実行することをお勧めします。

- 更新プロセスを容易にし、マージ競合の量を減らすような方法でアプリケーションを設計することに関して、JHipsterコミュニティからいくつかの有用なアプローチがあります。[JHipsterのSide-by-Sideアプローチ](https://www.youtube.com/watch?v=Gg5CYoBdpVo)の使用をお勧めします。

<h2 id="manual_upgrade">選択2 - 手動アップグレード</h2>

手動アップグレードの場合は、まず次のコマンドを使用してJHipsterのバージョンをアップグレードします。

```
npm install -g generator-jhipster
```

プロジェクトの`node_modules`フォルダを削除し、次のコマンドを実行します。

```
jhipster
```

次のコマンドの実行で、プロジェクトとそのすべてのエンティティの更新もできます。

```
jhipster --force
```

また、エンティティサブジェネレータを再度実行して、エンティティの1つずつの更新もできます。たとえば、エンティティの名前が _Foo_ の場合は次のとおりです。

```
jhipster entity Foo
```

### 名前を変更したファイルに関するヒント

ジェネレータ内でファイルの名前が変更されることがあります。Gitの名前変更の検出結果を確認したい場合は、`git add`（`git add .` で全てをステージングへ）を実行し、その後の変更をお気に入りのGitクライアントで確認できます。

多くのファイルの名前が変更された場合、Gitの名前変更の検出が期待通りに動作するように、Git設定の`diff.renameLimit`を増やしたい場合があります。例えば、`git config --replace-all diff.renameLimit 10000`です。

デフォルトでは、Gitの名前変更の検出は50％の類似性しきい値を使用します。名前が変更されたファイルの類似度を低くするには、Gitコマンドでオプション`--find-renames=<n>`を使用できます。たとえば、`git diff --staged --find-renames=30`です。

### 独自の変更を表示

プロジェクトの生成後に行った変更を確認するには、次の手順に従います。

`git clone`を使用して、プロジェクトを新しいフォルダにクローンします。

`.git`、`.jhipster`および`.yo-rc.json`を除くすべてのファイルとフォルダをクローンプロジェクトから削除します。

前回プロジェクトを生成したときに使用したJHipsterのバージョンを調べます。プロジェクトルートフォルダの`.yo-rc.json`を見て、`jhipsterVersion`の値を調べます。

前回プロジェクトを生成したときに使用したバージョンのJHipsterをインストールします。

```
npm install -g generator-jhipster@前回使用したJHipsterのバージョン
```

プロジェクトを再生成します。

```
jhipster --force --skip-install
```

`git diff`を使用すると、すべての変更が打ち消し（revert）された状態として確認できます。すべての変更を追加（add）された状態として確認したい場合は、すべてをGitにコミットしてから、前回のコミットを打ち消しします。

### JHipsterの変更点を参照

JHipsterによる変更を確認したい場合は、以下の手順に従ってください。

前回プロジェクトの生成に使用したJHipsterバージョンでプロジェクトを生成します。
* 新しいフォルダを作成します。
* プロジェクト`.yo-rc.json`ファイルと`.jhipster`フォルダをこの新しいフォルダにコピーします。
* 前回プロジェクトを生成したときに使用したJHipsterのバージョンを調べます。`.yo-rc.json`を見て、`jhipsterVersion`の値を調べます。
* 前回プロジェクトの生成に使用したJHipsterのバージョンをインストールします：`npm install-g generator-jhipster@前回使用したJHipsterのバージョン`
* 作成したフォルダで、次のコマンドを実行します：`jhipster --skip-install`

最新のJHipsterでプロジェクトを生成します。
* 新しいフォルダを作成します。
* プロジェクト`.yo-rc.json`ファイルと`.jhipster`フォルダをこの新しいフォルダにコピーします。
* 最新のJHipsterバージョンをインストールします：`npm install -g generator-jhipster`
* 作成したフォルダで、次のコマンドを実行します：`jhipster --skip-install`

これらの2つのフォルダをお好きなファイルおよびフォルダ比較ツールと比較して、JHipsterによって行われた変更を確認します。
