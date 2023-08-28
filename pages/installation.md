---
layout: default
title: JHipsterのインストール
permalink: /installation/
redirect_from:
  - /installation.html
sitemap:
    priority: 0.7
    lastmod: 2018-08-30T08:20:00-00:00
---

# <i class="fa fa-cloud-download"></i> JHipsterのインストール

## インストールの種類

JHipsterでは、4つの方法を用意しています。迷ったら、2番目の「NPMによるローカルインストール」を選んでください。

<<<<<<< HEAD
* [JHipster Online](https://start.jhipster.tech/)は、JHipsterをインストールせずにアプリケーションを生成するための方法です。
* 「NPMによるローカルインストール」は、JHipsterで作業する本格的な方法です。すべてはあなたのマシンにインストールされ、セットアップが少し複雑になりますが、ほとんどの人は通常この方法で作業します。迷ったらこのインストールを選択してください。
* 「Yarnによるローカルインストール」は、本格的な「NPMによるローカルインストール」と同じですが、NPMの代わりに [Yarn](https://yarnpkg.com/) を使用します。Yarnは私たちのコミュニティではNPMに比べてあまり使われておらず、初心者にはお勧めできない選択であることに注意してください。
* 「[Docker](https://www.docker.io/)」コンテナは、JHipsterがインストールされた軽量コンテナを提供する方法です。
=======
*   [JHipster Online](https://start.jhipster.tech/) is a way to generate an application without installing JHipster in the first place.
*   "Local installation with NPM" is the classical way of working with JHipster. Everything is installed on your machine, which can be a little complex to set up, but that's how most people usually work.
*   The "[Docker](https://www.docker.io/)" container, which brings you a lightweight container with JHipster installed.
>>>>>>> upstream/main

## JHipster Online (JHipsterを簡単に実行したいユーザー向け)

[JHipster Online](https://start.jhipster.tech/)は、JHipsterをインストールすることなく、JHipsterアプリケーションを生成できます。

初めてJHipsterを試す方や、JHipsterがどのようなものかを見てみたい方を対象としています。

アプリケーションを生成した後も、Java（アプリケーションの実行）とNPM（フロントエンドのコードの管理）が必要です。したがって、次のセクション（「NPMによるローカルインストール」）の手順のほとんどを実行する必要があります。

今後は、JHipster Onlineがより多くの機能を提供することを期待しています。

## NPMによるローカルインストール（一般ユーザー向け推奨）

### クイックセットアップ

1. Java 11をインストールします。オープンソースで無償のため、[Eclipse Temurin builds](https://adoptium.net/temurin/releases/?version=11)を使用することをお勧めします。
2. [Node.jsのウェブサイト](http://nodejs.org/)からNode.jsをインストールします（LTSの64ビット版を使用してください、LTS以外のバージョンはサポートされていません）。
3. `npm install -g generator-jhipster`でJHipsterをインストールします。
4. （オプション）モジュールやブループリントを使用したい場合（例えば[JHipster Marketplace]({{ site.url }}/modules/marketplace/#/list)から取得）`npm install -g yo`で[Yeoman](https://yeoman.io/) をインストールします。

JHipsterがインストールされました。次のステップは[アプリケーションの作成]({{ site.url }}/creating-an-app/)です。

### オプションのインストール

1. Javaビルドツールをインストールします。
    * [Maven](http://maven.apache.org/)、[Gradle](http://www.gradle.org/)のどちらを使うにしても、通常は何もインストールする必要はありません。JHipsterは自動的に[Maven Wrapper](https://github.com/takari/maven-wrapper) や [Gradle Wrapper](http://gradle.org/docs/current/userguide/gradle_wrapper.html) をインストールしてくれます。
    * もし、これらのラッパーを使用したくない場合は、公式の [Maven ウェブサイト](http://maven.apache.org/) または [Gradle ウェブサイト](http://www.gradle.org/) にアクセスして、自分でインストールを行ってください。
2.  [git-scm.com](http://git-scm.com/)からGitをインストールします。Gitを始める場合は、[SourceTree](http://www.sourcetreeapp.com/)のようなツールも使用することをお勧めします。
    * JHipsterは、Gitがインストールされている場合、プロジェクトをGitにコミットしようとします。
    * [JHipster upgrade sub-generator]({{ site.url }}/upgrading-an-application/) は、Gitをインストールしておく必要があります。

### 追加情報

JHipsterは、コード生成に[Yeoman](http://yeoman.io/)を使用しています。
より多くの情報、ヒント、ヘルプを見つけるには、[バグを報告する](https://github.com/jhipster/generator-jhipster/issues?state=open)前に[Yeoman "getting starting" guide](http://yeoman.io/learning/index.html) を参照してください。

設定は生成された `.yo-rc.json` ファイルに保存します。そのため、HOMEディレクトリにJHipsterプロジェクトを生成しないことを **強く** 推奨します。もしそうしてしまうと、サブディレクトリに別のプロジェクトを生成できなくなります。これを解決するには、`.yo-rc.json`ファイルを削除してください。

<<<<<<< HEAD
## Yarnによるローカルインストール (NPM の代替)

### クイックセットアップ

これは、NPMを使うのと同じ手順ですが、2つの違いがあります。

1. [Yarnのウェブサイト](https://yarnpkg.com/en/docs/install)からYarnをインストールします。
2. `yarn global add generator-jhipster`でJHipsterをインストールします。 

### トラブルシューティング

Yarnをグローバルに使用する際、問題がある場合は、`$HOME/.config/yarn/global/node_modules/.bin`がパスに入っていることを確認してください。

MacまたはLinuxの場合```export PATH="$PATH:`yarn global bin`:$HOME/.config/yarn/global/node_modules/.bin"```を実施します。

## Dockerのインストール（上級者向けのみ）
=======
## Docker installation (for advanced users only)
>>>>>>> upstream/main

_このDockerイメージは、JHipsterジェネレータをコンテナ内で動作させるためのものであることに注意してください。JHipsterが生成する[DockerとDocker Composeの設定]({{ site.url }}/docker-compose/) とは全く異なります。これは生成したアプリケーションをコンテナ内で実行することが目的です。_

### 情報

JHipsterは固有の[Dockerfile](https://github.com/jhipster/generator-jhipster/blob/main/Dockerfile)を持っており、[Docker](https://www.docker.io/)イメージを生成できます。

またJHipsteは[https://hub.docker.com/r/jhipster/jhipster/](https://hub.docker.com/r/jhipster/jhipster/)上で"Automated build"を提供しています。

このイメージにより、Docker内でJHipsterを動作させることができます。

### 前提条件

1.  **Docker Desktop(推奨）:** Docker化されたアプリを構築、実行、テストするための最も簡単な方法です。[Docker Desktop](https://docs.docker.com/desktop/)には、コンテナ/イメージ/ボリュームを管理するためのグラフィカルインタフェース、Docker開発者ツール、Kubernetesサポート、その他多くの機能が付属しています。
2.  **Docker Engine:** コマンドラインインタフェース（CLI）を持つクライアント／サーバーアプリケーションです。[Docker Engine](https://docs.docker.com/engine/install/)のインストール手順に従ってください。

生成されたファイルは共有フォルダにあるため、Dockerコンテナを停止しても削除されることはありません。ただし、コンテナを起動するたびにDockerにMavenとNPMの依存関係をすべてダウンロードさせ続けたくない場合は、その状態をコミットするかボリュームをマウントする必要があります。

<div class="alert alert-warning"><i>注意: </i>

お使いのOSによって<code>DOCKER_HOST</code>は異なります。Linuxの場合はlocalhostとなります。
Mac/Windowsの場合は、<code>docker-machine ip default</code>のコマンドでIPを取得する必要があります。

</div>

Linuxでは、自分のユーザがdockerグループに属していない場合、rootユーザとして`docker`コマンドを実行することになります。そこで、自分のユーザーをdockerグループに追加し、非rootユーザーとしてdockerコマンドを実行できるようにするとよいでしょう。そのためには、[http://askubuntu.com/a/477554](http://askubuntu.com/a/477554)の手順に従ってください。

### Linux/Mac Windowsでの使用方法（Dockerを使用した場合）

#### イメージのPull

最新のJHipsterのDockerイメージをPullします。

`docker image pull jhipster/jhipster`

開発用JHipsterのDockerイメージをPullします。

`docker image pull jhipster/jhipster:master`

すべてのタグは[こちら](https://hub.docker.com/r/jhipster/jhipster/tags/)です。

#### イメージを実行する

<div class="alert alert-warning"><i>注意:</i>

MacまたはWindowsでDocker Machineを使用している場合、DockerデーモンはOS XまたはWindowsのファイルシステムに対して限られたアクセスしかできません。Docker Machineは/Users (OS X)やC:\Users\&lt;username&gt; (Windows)ディレクトリを自動で共有しようとします。そのため、ボリュームマウントの問題を避けるために、これらのディレクトリの下にプロジェクトフォルダを作成する必要があります。

</div>


ホームディレクトリに「jhipster」フォルダを作成します。

`mkdir ~/jhipster`

以下のオプションを指定して、Dockerイメージを実行します。

* Dockerの"/home/jhipster/app"フォルダをローカルの"~/jhipster"フォルダに共有します。
* Dockerが公開する全てのポート（Javaアプリケーションは8080、BrowserSyncは9000、BrowserSync UIは3001）をフォワードします。

`docker container run --name jhipster -v ~/jhipster:/home/jhipster/app -v ~/.m2:/home/jhipster/.m2 -p 8080:8080 -p 9000:9000 -p 3001:3001 -d -t jhipster/jhipster`

<div class="alert alert-info"><i>Tip:</i>

過去に一度でもコンテナを起動している場合は、上記コマンドを実行する必要はなく、既存のコンテナを起動/停止できます。

</div>

#### コンテナが起動しているかどうかを確認する

コンテナが起動していることを確認するには、`docker container ps`コマンドを使用します。

    CONTAINER ID    IMAGE               COMMAND                 CREATED         STATUS          PORTS                                                       NAMES
    4ae16c0539a3    jhipster/jhipster   "tail -f /home/jhipst"  4 seconds ago   Up 3 seconds    0.0.0.0:9000-3001->9000-3001/tcp, 0.0.0.0:8080->8080/tcp    jhipster

#### 共通的な操作

* コンテナ実行を停止する場合`docker container stop jhipster` を実行します。
* そのあと起動するには`docker container start jhipster` を実行します。

Dockerイメージを更新する場合（リビルドまたはDocker hubからのPull）、既存のコンテナを削除し、コンテナを一から実行する方がよいでしょう。そのためには、まずコンテナを停止し、それを削除してから再度実行します。

1.  `docker container stop jhipster`
2.  `docker container rm jhipster`
3.  `docker image pull jhipster/jhipster`
4.  `docker container run --name jhipster -v ~/jhipster:/home/jhipster/app -v ~/.m2:/home/jhipster/.m2 -p 8080:8080 -p 9000:9000 -p 3001:3001 -d -t jhipster/jhipster`

### コンテナにアクセスする

<div class="alert alert-warning"><i>注意:</i>

Windowsでは、Docker Quick TerminalをAdministratorで実行しないと、`npm install`のステップでシンボリックリンクを作成できません。

</div>

実行中のコンテナにログインする最も簡単な方法は、以下のコマンドを実行します。

`docker container exec -it <コンテナ名> bash`

上記のコマンドをコピーペーストしてコンテナを実行した場合、コンテナ名として `jhipster` を指定する必要があることに注意してください。

`docker container exec -it jhipster bash`

"jhipster" ユーザーでログインします。

Ubuntu Xenialでは`sudo`コマンドが使えないので、"root"でログインしたい場合は、以下のようにする必要があります。

`docker container exec -it --user root jhipster bash`

### あなたの最初のプロジェクト

コンテナ内の/home/jhipster/appディレクトリに移動し、Docker内部でアプリの構築を開始できます。

`cd /home/jhipster/app`

`jhipster`

<<<<<<< HEAD
<div class="alert alert-info"><i>ヒント:</i>

Yarnを使用したい場合は、<code>jhipster --yarn</code> により、NPMの代わりにYarnを使用できます。

</div>

アプリケーションが作成されたら、以下のように、通常のgulp/bower/mavenのコマンドをすべて実行できます。
=======
Once your application is created, you can run all the normal gulp/bower/maven commands, for example:
>>>>>>> upstream/main

`./mvnw`

**おめでとうございます。Docker内でJHipsterアプリを起動できました。**

あなたのマシンにおいて以下が可能です。

* `http://DOCKER_HOST:8080`で実行中のアプリケーションにアクセスできます。
* 生成されたすべてのファイルを共有フォルダ内で参照できます。

<div class="alert alert-warning"><i>Warning:</i>
    デフォルトでは、<code>jhipster/jhipster</code>イメージ内にDockerはインストールされません。
    <br/>
    したがって以下は実施できません。
    <ul>
        <li>docker-composeのファイルを使用すること</li>
        <li>dockerデーモンでDockerイメージを構築すること（Mavenゴール：<code>jib:dockerBuild</code>またはGradleタスク：<code>jibDockerBuild</code>）</li>
    </ul>
    ただし、<a href="https://github.com/GoogleContainerTools/jib">jib</a>のデーモンレスのモードを使えば、dockerデーモンにアクセスしなくてもdockerイメージを構築してレジストリにプッシュできます（Mavenゴール：<code>jib:build</code>またはGradleタスク：<code>jibBuild</code>)。 一方、アプリをビルドする前提条件としてdockerレジストリへ認証情報をセットアップする必要があります。詳しくは<a href="https://github.com/GoogleContainerTools/jib/tree/master/jib-maven-plugin#configuration">Jib プラグイン設定ドキュメント</a>を参照してください。
</div>
