---
layout: default
title: JHipsterレジストリ
permalink: /jhipster-registry/
sitemap:
    priority: 0.7
    lastmod: 2019-02-01T00:00:00-00:00
---

# <i class="fa fa-dashboard"></i> JHipsterレジストリ（**非推奨**-代わりにConsulを使用してください）

## 概観

JHipsterレジストリは、JHipsterチームによって提供されるランタイムアプリケーションです。JHipsterジェネレータと同様に、Apache 2ライセンスのオープンソースアプリケーションであり、ソースコードは[jhipster/jhipster-registry](https://github.com/jhipster/jhipster-registry)のJHipster組織の下のGitHubで入手できます。

JHipsterレジストリの主な目的は次の3つです。

- [Eurekaサーバ](https://cloud.spring.io/spring-cloud-netflix/spring-cloud-netflix.html)となり、アプリケーションのディスカバリサーバを提供します。このサーバは、利用可能なアプリケーションインスタンスの動的リストを維持および配布し、その後、マイクロサービスがHTTP要求のルーティングとロードバランシングを行うために使用されます。
- [Spring Cloud Configサーバ](https://cloud.spring.io/spring-cloud-config/spring-cloud-config.html)となり、すべてのアプリケーションにランタイムコンフィギュレーションを提供します。
- 管理サーバとなり、アプリケーションを監視および管理するためのダッシュボードを具備します。

これらの機能はすべて、最新のAngularベースのユーザインタフェースを備えた単一の便利なアプリケーションにパッケージ化されています。

![]({{ site.url }}/images/jhipster-registry-animation.gif)

## 概要

1. [導入](#installation)
2. [Eurekaによるサービスディスカバリ](#eureka)
3. [Spring Cloud Configによるアプリケーション設定](#spring-cloud-config)
4. [管理ダッシュボード](#dashboards)
5. [JHipsterレジストリのセキュリティ保護](#security)

<h2 id="installation">導入</h2>

### Springプロファイル

JHipsterレジストリは、通常のJHipster`dev`および`prod`Springプロファイルと、Spring Cloud Configの標準の`composite`を使用します（[公式ドキュメント](https://cloud.spring.io/spring-cloud-config/multi/multi__spring_cloud_config_server.html#composite-environment-repositories)を参照してください）。

その結果、次のようになります。

- `dev`プロファイルを使用すると、`dev`および`composite`プロファイルを使用してJHipsterレジストリが実行されます。`dev`プロファイルは、ファイルシステムからSpring Cloud構成をロードし、`src/main/resources/config/bootstrap.yml`ファイルで定義された実行ディレクトリに関連する`central-config`ディレクトリを検索します。
- `prod`プロファイルを使用すると、`prod`および`composite`プロファイルを使用してJHipsterレジストリが実行されます。`prod`プロファイルは、GitリポジトリからSpring Cloud構成をロードします。これはデフォルトでは[https://github.com/jhipster/jhipster-registry-sample-config](https://github.com/jhipster/jhipster-registry-sample-config)です。実際の使用では、このリポジトリは、`src/main/resources/config/bootstrap-prod.yml`ファイルで再構成するか、`spring.cloud.config.server.composite`Springプロパティを再構成することによって変更する必要があります。

JHipsterレジストリが実行されたら、`Configuration > Cloud Config`メニューで設定を確認できます。ログインできない場合は、JWT署名キーが正しく設定されていない可能性があります。これは、設定が適切でないことを示しています。

### 事前にパッケージ化されたJARファイルの使用

JHipsterレジストリは、[リリースページ](https://github.com/jhipster/jhipster-registry/releases)にある実行可能なJARファイルとして利用できます。

JARファイルをダウンロードし、使用したいプロファイルを用いた通常のJHipsterアプリケーションとして実行します（プロファイルに関する前のセクションを参照してください）。たとえば、`central-config`ディレクトリに格納されているSpring Cloud Config設定を使用して実行するには、次のようにします。

    java -jar jhipster-registry-<version>.jar --spring.security.user.password=admin --jhipster.security.authentication.jwt.secret=my-secret-key-which-should-be-changed-in-production-and-be-base64-encoded --spring.cloud.config.server.composite.0.type=native --spring.cloud.config.server.composite.0.search-locations=file:./central-config

起動時に、`JHIPSTER_SECURITY_AUTHENTICATION_JWT_SECRET`環境変数を使用するか、上記のような引数を使用して、レジストリにJWTシークレットキーを提供することが重要であることに注意してください。別の方法としてこの値を、（レジストリを含みすべてのアプリケーションによって起動時にロードされる）集中化された構成ソースの`application.yml`ファイルにも設定できます。

JHipster 5.3.0以降、新しい`jhipster.security.authentication.jwt.base64-secret`プロパティが追加されました。これはより安全ですが、
あなたがまだ古いリリースを使用している可能性があるため、このドキュメントでは`jhipster.security.authentication.jwt.secret`を使用しています。これらのプロパティの詳細については、[セキュリティドキュメント]({{ site.url }}/security/)を参照してください。

同様に、`prod`プロファイルを使用してレジストリを実行するには、次のように引数を設定に合わせて調整します。

    java -jar jhipster-registry-<version>.jar --spring.profiles.active=prod --spring.security.user.password=admin --jhipster.security.authentication.jwt.secret=my-secret-key-which-should-be-changed-in-production-and-be-base64-encoded --spring.cloud.config.server.composite.0.type=git --spring.cloud.config.server.composite.0.uri=https://github.com/jhipster/jhipster-registry-sample-config

    java -jar jhipster-registry-<version>.jar --spring.profiles.active=prod --spring.security.user.password=admin --jhipster.security.authentication.jwt.secret=my-secret-key-which-should-be-changed-in-production-and-be-base64-encoded --spring.cloud.config.server.composite.0.type=git --spring.cloud.config.server.composite.0.uri=https://github.com/jhipster/jhipster-registry --spring.cloud.config.server.composite.0.search-paths=central-config

### ソースからの構築

JHipsterレジストリは、[jhipster/jhipster-registry](https://github.com/jhipster/jhipster-registry)から直接クローン/フォーク/ダウンロードできます。JHipsterレジストリもJHipsterによって生成されたアプリケーションであるため、他のJHipsterアプリケーションと同様に実行できます。

- （Javaサーバとしては）`./mvnw`を、（フロントエンドの管理には）`npm start`を使用して開発環境で実行します。デフォルトでは`dev`プロファイルが使用され、[http://127.0.0.1:8761/](http://127.0.0.1:8761/)で使用可能です。
-`./mvnw -Pprod package`を使用してプロダクション環境でパッケージ化し、通常のJHipster実行可能JARファイルを生成します。その後、`dev`または`prod`Springプロファイルを使用してJARファイルを実行できます。例：`java-jar jhipster-registry-<version>.jar --spring.profiles.active=prod`

`dev`および`composite`プロファイルを使用するには、設定に`central-config`ディレクトリが必要なので、`java -jar jhipster-registry-<version>.jar --spring.profiles.active=dev`を実行する場合は、そのディレクトリを設定する必要があることに注意してください。

### Dockerの使用

DockerイメージからJHipsterレジストリを実行したい場合は、Docker Hubの[jhipster/jhipster-registry](https://hub.docker.com/r/jhipster/jhipster-registry/)で入手できます。このイメージを実行するためのdocker-composeファイルは、各マイクロサービスの`src/main/docker`ディレクトリ内にすでに存在します。

- `docker-compose -f src/main/docker/jhipster-registry.yml up`を実行して、JHipsterレジストリを起動します。これはDockerホストのポート`8761`で使用できるので、マシンで実行する場合は[http://127.0.0.1:8761/](http://127.0.0.1:8761/)となります。

JHipsterレジストリをDocker Composeで使用する方法の詳細については、[Docker Composeのドキュメント]({{ site.url }}/docker-compose/)を参照してください。

### クラウドでの実行

JHipsterレジストリインスタンスはクラウドで実行できます。これは本番環境では必須ですが開発環境でも役立ちます（ラップトップで実行する必要がなくなります）。

JHipsterレジストリをCloud FoundryまたはHerokuにデプロイする方法については、["プロダクション環境下でのマイクロサービス"のドキュメント]({{ site.url }}/microservices-in-production/)を参照してください。

<h2 id="eureka">Eurekaによるサービスディスカバリ</h2>

![]({{ site.url }}/images/jhipster-registry-eureka.png)

JHipsterレジストリは[Netflix Eurekaサーバ](https://github.com/Netflix/eureka)であり、すべてのアプリケーションにサービスディスカバリを提供します。

- これはマイクロサービスアーキテクチャにとって非常に有用です。これにより、ゲートウェイはどのマイクロサービスが利用可能で、どのインスタンスが起動しているかを知ることができます。
- モノリスを含むすべてのアプリケーションにとっては、Hazelcast分散キャッシュを自動的にスケーリングできる方法となります。[Hazelcastキャッシュドキュメント]({{ site.url }}/using-cache/)を参照してください。

<h2 id="spring-cloud-config">Spring Cloud Configを使用したアプリケーション設定</h2>

![]({{ site.url }}/images/jhipster-registry-spring-cloud-config.png)

JHipsterレジストリは[Spring Config Server](http://cloud.spring.io/spring-cloud-config/spring-cloud-config.html)です。アプリケーションが起動されると、最初にJHipsterレジストリに接続して設定を取得します。これはゲートウェイとマイクロサービスの両方に当てはまります。

この設定は、JHipsterの`application-*.yml`ファイルにあるようなSpring Boot設定ですが、中央サーバに格納されるため、管理が容易です。

起動時に、ゲートウェイとマイクロサービスアプリはレジストリの設定サーバにクエリを行い、ローカルプロパティをそこで定義されたもので上書きします。

2種類の設定ソースを利用できます（`spring.cloud.config.server.composite`プロパティで定義されています）。

- `native`設定。開発（JHipsterの`dev`プロファイルを使用）でデフォルトで使用され、ローカルファイルシステムを使用します。
- `Git`設定。プロダクション（JHipsterの`prod`プロファイルを使用）でデフォルトで使用され、Gitサーバに保存されます。これにより、通常のGitツールを使用して設定のタグ付け、ブランチ、ロールバックが可能になり、このユースケースでは非常に強力です。

一元化された設定を管理するには、設定ソースに`appname-profile.yml`ファイルを追加する必要があります。ここで、**appname**と**profile**は、設定するサービスのアプリケーション名と現在のプロファイルに対応します。
たとえば、`gateway-prod.yml`ファイルにプロパティを追加すると、それらのプロパティは**prod**プロファイルで起動された**gateway**という名前のアプリケーションに対してのみ設定されます。さらに、`application[-dev|prod].yml`で定義されたプロパティは、すべてのアプリケーションに対して設定されます。

GatewayルートはSpring Bootを使用して設定されるため、Spring Config Serverを使用しての管理もできます。たとえば、アプリケーション`app1-v1`を`v1`ブランチの`/app1`のURLにマップし、アプリケーション`app1-v2`を`v2`ブランチの`/app1`のURLにマップできます。これは、エンドユーザがダウンタイムを発生させることなくマイクロサービスをアップグレードするための良い方法です。

<h2 id="encryption">暗号化された構成値の使用</h2>

JHipsterレジストリには、構成値の暗号化と復号化を可能にする固有の`configuration > encryption`ページがあります。

構成値（データベース・パスワードなど）を暗号化するには、次の手順を実行する必要があります。

- [JCE](http://www.oracle.com/technetwork/java/javase/downloads/jce8-download-2133166.html)をダウンロードし、ダウンロードしたファイルの指示に従ってインストールします（これは、Oracle JDKを使用している場合にのみ必要です）。
- `bootstrap.yml`（`application.yml`ではありません）に`encrypt.key`プロパティを設定するか、対称鍵パスフレーズで`ENCRYPT_KEY`環境変数を使用します。

すべてが正しく設定されていれば、特定の`Configuration > Encryption`ページを使用できるはずです。また、`/config/encrypt`および`/config/decrypt`エンドポイントにPOSTリクエストを送信し、リクエストの`body`に操作したいテキストを含めることができます。

例：`curl localhost:8761/config/encrypt -d mypassword`

暗号化テキストは、`*.yml`設定ファイル内に`password= '{cipher}myciphertextafterencryotion'`の形式で配置する必要があり、クライアントに送信する前に設定サーバによって復号化されます。これにより、設定ファイル（Gitに保存されているか、ファイルシステムに「ネイティブに」保存されている）にはプレーンテキストの値が含まれなくなります。

詳細については、Spring Cloud Configの[暗号化と復号化についてのドキュメント](http://cloud.spring.io/spring-cloud-config/spring-cloud-config.html#_encryption_and_decryption)を参照してください。

<h2 id="dashboards">管理ダッシュボード</h2>

JHipsterレジストリは、すべてのアプリケーションタイプに使用される管理ダッシュボードを提供します。アプリケーションがEurekaサーバに登録されるとすぐに、ダッシュボードで使用可能になります。

アプリケーションから機密情報にアクセスするために、JHipsterレジストリはJWTトークンを使用します（これが、JHipsterレジストリがJWTを使用するアプリケーションに対してのみ機能する理由です）。リクエストの署名に使用されるJWTキーは、アプリケーションとJHipsterレジストリで同じである必要があります：デフォルトでは、JHipsterレジストリはSpring Cloud Configを介してアプリケーションを設定するため、すべてのアプリケーションに同じキーを送信するため、これはすぐに使用できるはずです。

### メトリクスダッシュボード

![]({{ site.url }}/images/jhipster-registry-metrics.png)

メトリクスダッシュボードは、Micrometerを使用して、アプリケーションパフォーマンスの詳細なビューを提供します。

次のメトリクスが表示されます。

- JVM
- HTTPリクエスト
- キャッシュの使用状況
- データベース接続プール

JVMスレッド・メトリクスの横にある展開ボタンをクリックすると、実行中のアプリケーションのスタック・トレースが表示されます。これは、ブロックされているスレッドを見つけるのに非常に役立ちます。

注意：JHipsterレジストリをDropwizardメトリクスではなくMicrometerからのメトリクスを監視するように変更したので、バージョン5.7.2以前で生成されたすべてのJHipsterアプリケーションをMicrometerに移行して、JHipsterレジストリで監視する必要があります。アプリケーションを移行しない場合は、JHipsterレジストリv4.0.6以前を使用してください。

アプリケーションを移行するには、[JHipsterアップグレード・サブジェネレーター]({{ site.url }}/upgrading-an-application/)を使用できます。

### ヘルスダッシュボード

![]({{ site.url }}/images/jhipster-registry-health.png)

ヘルスダッシュボードは、Spring Boot Actuatorのヘルスエンドポイントを使用して、アプリケーションのさまざまな部分のヘルス情報を提供します。
多くのヘルスチェックは、Spring Boot Actuatorによってすぐに使用できる状態で提供され、アプリケーション固有のヘルスチェックを追加できます。

### 設定ダッシュボード

![]({{ site.url }}/images/jhipster-registry-configuration.png)

設定ダッシュボードは、Spring Boot Actuatorの設定エンドポイントを使用して、現在のアプリケーションのSpring設定の完全なビューを提供します。

### ログダッシュボード

![]({{ site.url }}/images/jhipster-registry-logs.png)

ログダッシュボードを使用すると、実行中のアプリケーションのLogback設定を実行時に管理できます。
Javaパッケージのログ・レベルを変更するには、ボタンをクリックします。これは、開発環境と本番環境の両方で非常に便利です。

<h2 id="security">JHipsterレジストリの保護</h2>

JHipsterレジストリはデフォルトで保護されています。通常のJHipsterアプリケーションで使用される通常の"admin/admin"ログインおよびパスワードを使用してログインできます。

アプリケーションも同じ"admin"ユーザを使用してJHipsterレジストリに接続しますが、HTTP Basic認証を使用します。マイクロサービスがレジストリにアクセスできず、"401 authentication error"メッセージが表示される場合は、それらのアプリケーションの設定が間違っていることが理由です。

JHipsterレジストリを保護するには、次の手順を実行します。

- デフォルトの"admin"パスワードを変更する必要があります。このパスワードは標準のSpring Bootプロパティ`spring.security.user.password`を使用して設定されるため、通常のSpring Bootメカニズムを使用して変更できます。プロジェクトの`application-*.yml`ファイルを変更するか、`SPRING_SECURITY_USER_PASSWORD`環境変数を追加できます。[Docker Composeサブジェネレータ]({{ site.url }}/docker-compose/)は環境変数で設定する方法を使用します。
- あなたのアプリケーションはHTTPを使用してレジストリに接続するので、その接続チャネルを保護することは非常に重要です。それを行う方法はたくさんありますが、おそらく最も簡単なのはHTTPSを使用することです。
