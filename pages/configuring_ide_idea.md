---
layout: default
title: Intellij IDEAの設定
permalink: /configuring-ide-idea/
redirect_from:
  - /configuring_ide_idea.html
sitemap:
    priority: 0.7
    lastmod: 2015-11-28T17:13:00-00:00
---

# <i class="fa fa-keyboard-o"></i> Intellij IDEAの設定

## プロジェクトを開く

- プロジェクトを通常通り開きます。
- Mavenが検出され、プロジェクトが自動的にビルドされるはずです。

セットアップをよりコントロールしたい場合は、「プロジェクトのインポート」を選択できます。

## 除外するディレクトリ

Gitを使用している場合、プロジェクトの初期化（`git init && git add . && git commit -m 'Initial commit'`）を行うと、Intellij IDEAはGitが無視するディレクトリを自動的に除外します（つまり、あなたは何もする必要がありません）。

手動でディレクトリを除外する場合は以下のとおりです。

- `node_modules/`フォルダを右クリックします。
- "Mark Directory As"を選択し、"Excluded"を選択します。

![除外]({{ site.url }}/images/configuring_ide_idea_1.png)

**注意:** Intellij IDEA Ultimateを使用していて、IDEAでフロントエンドをコーディングしたい場合は、`node_modules`フォルダを**除外する必要はありません**。もし除外してしまうと
フロントエンドのコードのアシストを受けられなくなります。

## Spring サポート (Community Edition では利用できません)

新しいプロジェクトでJHipsterの多くのモジュールにSpringサポートを追加するには、まず`File → Project Structure`に進みます。

![プロジェクト構成]({{ site.url }}/images/configuring_ide_idea_2.png)

次にモジュールタブを開き、`+`ボタンをクリックし、"Spring"をクリックして、プロジェクトにSpringコードアシストを追加します。

![Spring]({{ site.url }}/images/configuring_ide_idea_3.png)

右下の`+`記号（本来の記号ではありません）をクリックして、プロジェクトに属するすべてのSpringファイルを選択してください、フォルダをクリックするだけですべてが選択されます。

![Spring Application Context]({{ site.url }}/images/configuring_ide_idea_4.png)

その後、`OK`をクリックすると、Springが適切なコードアシストで構成されるはずです。

次に、最初にSpringを追加するために使用した元の`+`ボタンをクリックし、Hibernateを追加します。
Hibernateを追加することで、Hibernateベースのコードアシストが得られるので、ここではファイルを追加する必要はありません。プロジェクト構造ダイアログで`OK`をクリックするのを忘れないようにしましょう。

これで、コードベースのほとんどでSpringがサポートされるようになったはずです。なお、これらの設定はプロジェクト固有のため、新しいプロジェクトを始めるたびにこのステップを繰り返す必要があります。

## Spring Bootのdevtoolsを使ったアプリケーションの「ホットリスタート」

[Spring Boot devtools](https://docs.spring.io/spring-boot/docs/current/reference/html/using-boot-devtools.html)はJHipsterによって設定され、プロジェクトからのクラスがコンパイルされると、アプリケーションを「ホットリスタート」します。これはアプリケーションがその場で更新されるようになる必須の機能です。

デフォルトでは、IntelliJ IDEAは、アプリケーションの実行時にファイルを自動的にコンパイルしません。「保存時にコンパイルする」機能を有効にするには、以下のようにします。

* `File → Settings → Build, Execution, Deployment → Compiler` に行き、"Make project automatically"を有効にします。
* Action windowを開きます。
  * Linux : `CTRL+SHIFT+A`
  * Mac OSX : `SHIFT+COMMAND+A`
  * Windows : `CTRL+ALT+SHIFT+/`
* `Registry...`に入り`compiler.automake.allow.when.app.running`を有効にします。

注意：IntelliJ IDEA version 2021.2では以下のようにします。
* `File → Settings → Build, Execution, Deployment → Compiler`に行き、"Build project automatically"を有効にします。
* `File → Advanced Settings → Compiler`に行き、"Allow auto-make to start even if developed application is currently running"を有効にします。

## Maven IDEプロファイル

Mavenを使用している場合、IntelliJで`IDE`プロファイルを有効にする必要があります。これはIDE固有の調整を適用するために使用されます。
現在はMapStructアノテーション・プロセッサーを適用することだけが含まれています。

"Maven Projects"ツールウィンドウ（View → Tool Windows）を開き、`IDE`のmaven profileにチェックを入れて有効にします。

## Gradle

Gradleですぐに開発できる最高の体験を得るためには、すべての[IDEビルド/ランアクションをGradleに](https://www.jetbrains.com/idea/whatsnew/#v2017-3-gradle)直接委ねるべきです。この設定により、アノテーション処理が自動的に設定され、IDEとcliのビルドを混在させても、重複したクラスが発生することはありません。古いバージョン（2016.3より前）を使用している場合は、手動でアノテーション処理を有効にする必要があります。
