---
layout: default
title: Herokuへのデプロイ
permalink: /heroku/
redirect_from:
  - /heroku.html
sitemap:
    priority: 0.7
    lastmod: 2023-12-19T00:00:00-00:00
---

# Herokuへのデプロイ

このサブジェネレータを使用すると、JHipsterアプリケーションを[Herokuクラウド](https://www.heroku.com/){:target="_blank" rel="noopener"}にデプロイできます。

[![]({{ site.url }}/images/logo/logo-heroku.png)](https://www.heroku.com/){:target="_blank" rel="noopener"}


## サブジェネレータの実行

サブジェネレータを実行する前に、[Heroku CLI](https://cli.heroku.com/){:target="_blank" rel="noopener"}をインストールする必要があります。

また、[Herokuアカウントの作成](http://signup.heroku.com/){:target="_blank" rel="noopener"}を実行し、次のコマンドを実行してCLIでログインする必要があります。

<pre>**$ heroku login**
Enter your Heroku credentials.
Email: YOUR_EMAIL
Password (typing will be hidden): YOUR_PASSWORD
Authentication successful.
</pre>

<div class="alert alert-warning"><i class="fa fa-money" aria-hidden="true"></i>
<<<<<<< HEAD
2022年11月より、<a href="https://blog.heroku.com/next-chapter" target="_blank" rel="noopener">Herokuは完全に無料のプランを提供しなくなりました</a>。
これは、<a href="https://devcenter.heroku.com/articles/account-verification" target="_blank" rel="noopener">適切に認証されたHerokuアカウント</a>が必要であることを意味します。
そして、最小限のdynoオプションと最小サイズのPostgresを使用してアプリケーションをデプロイする場合、費用は<b>月額約12ドル</b>になります。
=======
As of <a href="https://blog.heroku.com/next-chapter" target="_blank" rel="noopener">>November 2022 Heroku does not offer a completely free tier</a> anymore.
This means you will need a properly <a href="https://devcenter.heroku.com/articles/account-verification" target="_blank" rel="noopener">verified Heroku account</a>
and deploying an application using the smallest dyno options and the smallest Postgres size will cost you around <b>$12 per month</b>.
>>>>>>> upstream/main
</div>

Herokuサブジェネレータは、選択した構成に一致するアドオンを使用した[free dynos](https://devcenter.heroku.com/articles/dyno-types){:target="_blank" rel="noopener"}を使用してアプリケーションを作成します。

次のアドオンをサポートしています。

* [Heroku Postgres](https://www.heroku.com/postgres){:target="_blank" rel="noopener"}：PostgreSQLの使用
* [JawsDB](https://elements.heroku.com/addons/jawsdb){:target="_blank" rel="noopener"}：MySQLまたはMariaDBの使用
* [Heroku Redis](https://elements.heroku.com/addons/heroku-redis){:target="_blank" rel="noopener"}：[Redisの使用](/using-cache/#caching-with-redis)
* [MemCachier](https://elements.heroku.com/addons/memcachier){:target="_blank" rel="noopener"}：[Memcachedの使用](/using-cache/#caching-with-memcached)
* [Bonsai Elasticsearch](https://elements.heroku.com/addons/bonsai){:target="_blank" rel="noopener"}：[Elasticsearchの使用](/using-elasticsearch/)
* [Okta](https://elements.heroku.com/addons/okta){:target="_blank" rel="noopener"}：[OAuth2/OIDC（オプション）の使用](/security/#oauth2)


アプリケーションをHerokuにデプロイするには、次のコマンドを実行します。

`jhipster heroku`

これにより、アプリケーションが「プロダクション」モードでパッケージ化され、データベースを持つHerokuアプリケーションが作成され、コードがアップロードされ、アプリケーションが起動されます。

<div class="alert alert-info"><i class="fa fa-info-circle" aria-hidden="true"></i>
アプリケーションがマイクロサービスの場合は、レジストリURLを指定するように求められることに注意してください。これを行う方法については、下にスクロールしてください。
</div>

<div class="alert alert-warning"><i class="fa fa-exclamation-circle" aria-hidden="true"></i>
アプリケーションは90秒以内に起動する必要があります。起動しない場合はシャットダウンされます。
プラットフォームの負荷によっては、90秒未満での開始は保証されません。
</div>

## Javaバージョンの変更

Herokuサブジェネレータの実行時にJavaバージョンを選択できます。
デフォルトでは、Java 11です。
Heroku[公式ドキュメントでサポートされているJavaバージョン](https://devcenter.heroku.com/articles/java-support#supported-java-versions){:target="_blank" rel="noopener"}にすべて記載されています。

Javaのバージョンを例えば後で`11`から`14`に変更したい場合は、プロジェクトのルートフォルダの`system.properties`で変更する必要があります。

```
java.runtime.version=14
```

アプリケーションを再デプロイすると、Java 14が使用されます。

## アプリケーションの導入

デフォルトでは、アプリケーションは[git経由でデプロイされます](https://devcenter.heroku.com/articles/git){:target="_blank" rel="noopener"}。
これは、コードをプッシュすると、Herokuがそれをビルドしてサーバにデプロイすることを意味します。
コードを他のサーバーにプッシュできない場合、またはプッシュしたくない場合は、jarオプションを使用して[実行可能なjarをデプロイできます](https://devcenter.heroku.com/articles/deploying-executable-jar-files){:target="_blank" rel="noopener"}。
Herokuは[dockerイメージのデプロイ](https://devcenter.heroku.com/articles/container-registry-and-runtime){:target="_blank" rel="noopener"}もサポートしていますが、サブジェネレータはまだこのオプションをサポートしていません。

### 展開したアプリケーションの更新

#### gitオプションの使用

git経由でデプロイする場合、herokuと呼ばれる新しいリモートが作成されています。
新しいコードをデプロイするには、変更をherokuリモートにプッシュする必要があります。

`git push heroku master`

<div class="alert alert-info"><i class="fa fa-info-circle" aria-hidden="true"></i>
これは、このコマンドを実行するマシン上でジェネレータを実行したことを前提としています。
まだ作成していない場合は、<a href="https://devcenter.heroku.com/articles/git#for-an-existing-heroku-app" target="_blank" rel="noopener">の手順に従ってHerokuリモートを作成する必要があります。</a>.
</div>

#### jarオプションを使用

実行可能なjarをデプロイすることを選択した場合、更新されたjarを作成し、新しいファイルをHerokuにデプロイする必要があります。

##### 新しいJARの準備

アプリケーションがすでにデプロイされている場合は、次を使用して新しいデプロイを準備できます。

`./mvnw package -Pprod -DskipTests`

gradleを使用する場合は、次のように入力します。

`./gradlew -Pprod bootJar -x test`

##### 本番環境へのプッシュ配信

<div class="alert alert-info"><i class="fa fa-info-circle" aria-hidden="true"></i>
これは、このコマンドを実行するマシン上でジェネレータを実行したことを前提としています。
まだインストールしていない場合は、<a href="https://devcenter.heroku.com/articles/deploying-executable-jar-files" target="_blank" rel="noopener">Heroku Java CLI</a>のインストール手順に従う必要があります。
</div>

本番にプッシュするには、次のように入力します。

`heroku deploy:jar target/*.jar`

gradleを使用する場合は、次のように入力します。

`heroku deploy:jar build/libs/*jar`

## HerokuへのDockerのデプロイ

アプリをDockerコンテナとしてHerokuにデプロイもできます。これは動作しますが、Herokuのセットアップや設定は行われないため、手動で行う必要があります。このドキュメントでは、すでに`jhipster heroku`を実行してアプリをデプロイしていることを前提としているため、このプロセスが実行する統合とアドオンのプロビジョニングを活用しています。

**注**:v6.10.2より前のバージョンのJHipsterを使用している場合は、`src/main/resources/config/application-heroku.yml`に次の内容を追加する必要があります。

```yaml
server:
  port: ${PORT:8080}
```

Dockerイメージをビルドします。

```
./mvnw package -Pprod verify jib:dockerBuild
```

Gradleを使用している場合は、次のように入力します。

```
./gradlew -Pprod bootJar jibDockerBuild
```

Docker Composeを使ってローカルでテストができます。

```shell
docker-compose -f src/main/docker/app.yml up
```

すべてが動作することを確認したら、Herokuで新しいアプリを作成し、それをリモートとして追加します。

```shell
heroku apps:create
git remote add docker https://git.heroku.com/<your-new-app>.git
```

次に、以下のコマンドを実行して、JHipsterアプリをDockerイメージとしてデプロイします。`<...>`プレースホルダをHerokuアプリ名に置き換えてください。アプリ名がわからない場合は、`heroku apps`を実行してください。

```shell
heroku container:login
docker tag space registry.heroku.com/<heroku-app>/web
docker push registry.heroku.com/<heroku-app>/web
```

次に例を示します。

```shell
heroku container:login
docker tag space registry.heroku.com/fast-peak-70014/web
docker push registry.heroku.com/fast-peak-70014/web
```

この時点で、すでに設定したPostgreSQLとOktaのアドオンを使用できます。最初に展開した`heroku`リモートからアドオンの識別子を取得するには、次のコマンドを実行します。

```shell
heroku addons --remote heroku
```

その後、これらのインスタンスを新しいアプリケーションにアタッチできます。

```shell
heroku addons:attach <postgresql-addon-name> --remote docker
heroku addons:attach <okta-addon-name> --remote docker
```

アプリケーションのデプロイに`jhipster heroku`を使用すると、データベースが適切に構成されます。ただし、Dockerコンテナとしてデプロイする場合は、そのようなことはありません。そのため、DockerコンテナがPostgreSQLと通信できるように、いくつかの設定変数を設定する必要があります。まず、次のコマンドを実行してPostgreSQL URLを取得します。

```
heroku config:get DATABASE_URL --remote docker
```

このコマンドは、次の構文で値を取得します。

```
postgres://username:password@address
```

次に、`application-heroku.yml`にあるキーと一致するようにデータベース環境変数を設定します。

```shell
heroku config:set JDBC_DATABASE_URL=jdbc:postgresql://<address> --remote docker
heroku config:set JDBC_DATABASE_USERNAME=<username> --remote docker
heroku config:set JDBC_DATABASE_PASSWORD=<password> --remote docker
```

使用するJavaメモリの最大量を設定し、Springプロファイルを指定します。

```shell
heroku config:set JAVA_OPTS=-Xmx256m
heroku config:set SPRING_PROFILES_ACTIVE=prod,heroku
```

次のコマンドを実行してブラウザを開き、アプリケーションに移動します。

```
heroku open --remote docker
```

あなたのアプリのURLをコピーして、あなたのOkta開発者アカウントにログインします。**Applications** > **Web** > **General** に移動して、ログインおよびログアウトリダイレクトURIにURLを追加します。ログインリダイレクトURIが`/login/oauth2/code/oidc`で終わることを確認してください。

これで、コンテナを解放してアプリを起動できるようになります。

```
heroku container:release web --remote docker
```

ログを監視して、コンテナが正常に起動したかどうかを確認できます。

```
heroku logs --tail --remote docker
```

これで、アプリを開き、**サインイン**リンクをクリックして、認証できるはずです!

```
heroku open --remote docker
```

**注**:Oktaアドオンが提供するadminアカウントを使用してJHipsterアプリにログインは**できません**。そのアカウントでログインしていないことを確認するために、新しいプライベートウィンドウを使用してログインすることをお勧めします。

Docker化されたJHipsterアプリを[securityheaders.com](https://securityheaders.com)でテストすると、**A**のスコアが出ます!

## マイクロサービスのデプロイ

JHipsterマイクロサービスには、[JHipsterでマイクロサービスを実行する](/microservices-architecture/)ドキュメントで説明されているように、ConsulまたはJHipsterレジストリが必要です。次のボタンをクリックすると、JHipsterレジストリをHerokuにデプロイできます。

[![Herokuにデプロイ](https://camo.githubusercontent.com/c0824806f5221ebb7d25e559568582dd39dd1170/68747470733a2f2f7777772e6865726f6b7563646e2e636f6d2f6465706c6f792f627574746f6e2e706e67)](https://dashboard.heroku.com/new?&template=https%3A%2F%2Fgithub.com%2Fjhipster%2Fjhipster-registry)

レジストリがデプロイされたら、マイクロサービスまたはゲートウェイに対して`jhipster heroku`コマンドを実行できます。HerokuサブジェネレータはレジストリのURLを要求します。このURLは`https://[appname].herokuapp.com`のような形式になります。

Herokuで実行されるレジストリには、次のようないくつかの制限があります。

*   レジストリはネイティブ設定でのみ動作します（Git設定では動作しません）。
*   レジストリサービスは、冗長性を提供する複数のdynosにスケールアップできません。複数のアプリケーションをデプロイする必要があります（つまり、ボタンを複数回クリックする必要があります）。これは、Eurekaがインスタンス間のメモリ内状態を同期するために個別のURLを必要とするためです。

### HerokuのJHipsterレジストリでセキュリティを使用する

JHipsterレジストリに自動的に生成されたadminパスワードを取得するには、次のように入力します。

`heroku config:get JHIPSTER_PASSWORD`

このパスワードを使用するには、次のコマンドを実行して、レジストリの資格情報を使用するように、すべてのマイクロサービスとゲートウェイを更新します。

`heroku config:set JHIPSTER_REGISTRY_URL="https://admin:[password]@[appname].herokuapp.com"`

## トラブルシューティング

Liquibaseの変更ログが適用されているときにアプリケーションがHerokuによって停止された場合、データベースはLiquibaseによって「ロック済み」とマークされます。ロックテーブルを手動でクリーンアップする必要があります。Postgresでは、[ローカルPostgresクライアントがインストールされている](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup){:target="_blank" rel="noopener"}ことを確認し、次のコマンドを実行します。

`heroku pg:psql -c "update databasechangeloglock set locked=false;"`

Herokuのデフォルトのブートタイムアウト制限は90秒です。アプリがこれより長くかかる場合、Herokuはプロセスを停止し、データベースがロック状態のままになる可能性があります。問題が解決しない場合は、[Herokuサポート](http://help.heroku.com){:target="_blank" rel="noopener"}に連絡して、アプリのブート制限を延長するよう依頼してください。

### Elasticsearchの使用

無料サンドボックスプランのBonsai usedアドオンは、[Elasticsearch 7.10.xのみをサポート](https://docs.bonsai.io/article/139-which-versions-bonsai-supports){:target="_blank" rel="noopener"}します。
これにより、使用しているSpring Dataと[JHipsterのバージョン](https://github.com/jhipster/generator-jhipster/issues/18650){:target="_blank" rel="noopener"}によっては、いくつかの[非互換性](https://github.com/jhipster/generator-jhipster/issues/10003){:target="_blank" rel="noopener"}が生じる可能性がります。
JHipsterは、Herokuにデプロイするとき、[bonsaiと互換性のあるElasticsearch依存関係（クライアントなど）を強制します](https://github.com/jhipster/generator-jhipster/pull/18774){:target="_blank" rel="noopener"} 

<div class="alert alert-warning"><i class="fa fa-money" aria-hidden="true"></i>
<b>有料</b>のアドオンを使用する場合は、<a href="https://devcenter.heroku.com/articles/foundelasticsearch" target="_blank" rel="noopener">公式のElastic Cloud統合</a>を使用して、最新のElasticsearchバージョンと機能にアクセスできます。
</div>

## 詳細情報

*   [適用例](https://github.com/kissaten/jhipster-example){:target="_blank" rel="noopener"}
*   [Spring Boot Herokuドキュメント](https://docs.spring.io/spring-boot/docs/current/reference/html/deployment.html#cloud-deployment-heroku){:target="_blank" rel="noopener"}
*   [Herokuフリーdynoドキュメント](https://devcenter.heroku.com/articles/free-dyno-hours){:target="_blank" rel="noopener"}
*   [Heroku Javaサポートドキュメント](https://devcenter.heroku.com/articles/java-support#supported-java-versions){:target="_blank" rel="noopener"}
