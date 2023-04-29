---
layout: default
title: JHipsterコントロールセンター
permalink: /jhipster-control-center/
sitemap:
    priority: 0.7
    lastmod: 2020-10-20T00:00:00-00:00
---

# <i class="fa fa-codepen"></i> JHipsterコントロールセンター

## 概観

JHipsterコントロールセンターの主な目的は、アプリケーションの監視と管理です。

そのすべての機能は、最新のVueユーザインタフェースを備えた1つの外部アプリケーションにパッケージ化されています。そのソースコードは、[jhipster/jhipster-control-center](https://github.com/jhipster/jhipster-control-center)のJHipster組織の下のGitHubで入手できます。

![]({{ site.url }}/images/jhipster-control-center-animation.gif)

## 概要

1. [特有のSpringプロファイル](#profiles)
2. [インストール](#installation)
3. [アーキテクチャ](#architecture)
4. [認証メカニズム](#authentication)
5. [機能](#features)

<h2 id="profiles"> 特有のSpringプロファイル</h2>

**コントロールセンターは、通常のJHipsterの`dev`および`prod`Springプロファイルを使用します。しかし、正しく動作するためには、Spring Cloud Discoveryバックエンドに対応するSpring Profileから開始する必要があります。**

- `eureka`: Eurekaサーバに接続し、application-eureka.ymlで設定された登録済みインスタンスを取得します。
- `consul`: Consulサーバに接続し、application-consul.ymlで設定された登録済みインスタンスを取得します。
- `static`: application-static.ymlで設定された、プロパティとして提供されるインスタンスの静的リストを使用します。
- `kubernetes`: application-kubernetes.ymlに設定されます。

これはマイクロサービスアーキテクチャにとって非常に有用です。これにより、コントロールセンターはどのマイクロサービスが利用可能で、どのインスタンスが起動しているかを知ることができます。

モノリスを含むすべてのアプリケーションにとっては、Hazelcast分散キャッシュを自動的にスケーリングできる方法となります。[Hazelcastキャッシュドキュメント]({{ site.url }}/using-cache/)を参照してください。

<h2 id="installation">インストール</h2>

### ローカルでの実行

* ### ステップ1：Spring Cloudディスカバリバックエンドで使用されるサーバを実行する

    EurekaとConsulのdocker-composeファイルはsrc/main/dockerの下にあり、プロジェクトのテストが容易に可能です（[特有のSpringプロファイル](#profiles)を参照）。

    - Consulの実行：`docker-compose -f src/main/docker/consul.yml up -d`
    - Eurekaの実行：`docker-compose -f src/main/docker/jhipster-registry.yml up -d`
    - Kubernetesについては[kubernetesのドキュメント](https://www.jhipster.tech/kubernetes/#deploying-to-kubernetes)を参照
    - それ以外の場合でインスタンスの静的リストを使用するには、直接次の手順に進みます。

* ### ステップ2：認証プロファイルを選択する

    認証には2つのタイプがあります（[認証メカニズム](#authentication)を参照）。

    - JWT：デフォルトの認証で、これを選択した場合は何もする必要はありません。
    - OAuth2：OAuth2認証を使用するには、Keycloakを起動する必要があります。`docker-compose -f src/main/docker/keycloak.yml up -d`を実行してください。
    

* ### ステップ3：複製したプロジェクトを実行する

    特有のSpringプロファイルに従って、コントロールセンターを実行します。次に例を示します。

    - JWTおよびConsulを使用した開発の場合、`./mvnw -Dspring.profiles.active=consul,dev`
    - JWTおよびEurekaを使用した開発の場合、`./mvnw -Dspring.profiles.active=eureka,dev`
    - JWTおよびインスタンスの静的リストを使用した開発の場合、`./mvnw -Dspring.profiles.active=static,dev`
    - OAuth2およびConsulを使用した開発の場合、`./mvnw -Dspring.profiles.active=consul,dev,oauth2`
    - OAuth2およびEurekaを使用した開発の場合`./mvnw -Dspring.profiles.active=eureka,dev,oauth2`
    - 開発環境で起動するには、`./mvnw`を実行し、別の端末では、クライアント側コードのホットリロード用に`npm start`を実行します。

### Dockerからの実行

コンテナイメージがDocker hubで利用可能となりました。これを使用するには、次のコマンドを実行します。

- `docker pull jhipster/jhipster-control-center`
- `docker run -d --name jhcc -p 7419:7419 jhipster/jhipster-control-center:latest`

<h2 id="architecture">アーキテクチャ</h2>

これは、管理APIエンドポイントを介して1つまたは複数のJHipsterアプリケーションに接続する標準のWebアプリケーションです。これらの管理エンドポイントは、標準のAPIポート（通常は8080, 8081, ...）や専用の管理ポート（通常は9999）で公開されることにより、外部から隔離されます。

コントロールセンターは[Spring Cloud Gateway](https://docs.spring.io/spring-cloud-gateway/docs/current/reference/html/)をルーティングAPIに使用し、Spring Cloud LoadBalancerを、別のマイクロサービスへの呼び出し時のクライアント側のロードバランシングのために使用します（Spring Cloud LoadBalancerによるロードバランシングの実装を使用するために、Ribbonはデフォルトで無効になっています）。

![]({{ site.url }}/images/jhipster-control-center-architecture.png)

<h2 id="authentication">認証メカニズム</h2>

アプリケーションにアクセスするために、JHipster Control Centerはプロファイルに応じた特有のセキュリティメカニズムを使用します。

#### ***JWT***
これはJHipster独自の実装です。リクエストの署名に使用されるJWTキーは、アプリケーションとコントロールセンターで同じである必要があります。デフォルトでは、コントロールセンターはSpring Cloud Configを使用してアプリケーションを設定し、すべてのアプリケーションに同じキーを送信するため、これはすぐに機能するはずです。

#### ***OAuth2***
このプロファイルは、Keycloak（もしくはそのうちOktaも）のようなサード・パーティの認可認証サーバーを使用します。コントロール・センターに接続すると、コントロール・センターはOAuth2プロトコルを使用してKeycloakでセッションを生成します。

次に、Oauth2SecurityConfiguration.javaのセキュリティ設定では、Spring Securityのフィルタチェインを使用してKeycloakから認可情報を取得し、`http.oauth2Login()`を使用してSpringのプリンシパル（現在のユーザー）を生成します。その後、Spring Securityのフィルタチェインは、`http.oauth2ResourceServer().jwt().jwtAuthenticationConverter(jwtAuthenticationConverter())`を適用して、彼のロールで認証を取得します。これにより、プロバイダ（Keycloak、Oktaなど）を簡単に変更できます。

<h2 id="features">機能</h2>

### ***インスタンス***

JHipsterコントロールセンターは、アプリケーションのインスタンスのリストを提供します。アプリケーションがサーバー（consulまたはeureka）に登録されるとすぐに、リストで使用可能になります。

![]({{ site.url }}/images/jhipster-control-center-instances.png)

### ***メトリクス***

メトリクスページでは、Micrometerを使用してアプリケーションパフォーマンスの詳細なビューを提供します。

次のメトリックが表示されます。

- JVM
- HTTPリクエスト
- キャッシュの使用状況
- データベース接続プール

JVMスレッド・メトリクスの横にある展開ボタンをクリックすると、実行中のアプリケーションのスタック・トレースが表示されます。これは、ブロックされているスレッドを見つけるのに非常に役立ちます。

![]({{ site.url }}/images/jhipster-control-center-metrics.png)

### ***稼働状態***

ヘルスページは、Spring Boot Actuatorのヘルスエンドポイントを使用して、アプリケーションのさまざまな部分の稼働状態の情報を提供します。

多くのヘルスチェックは、Spring Boot Actuatorによってすぐに使用できる状態で提供され、アプリケーション固有のヘルスチェックを追加できます。

![]({{ site.url }}/images/jhipster-control-center-health.png)

### ***設定***

設定ページでは、Spring Boot Actuatorの設定エンドポイントを使用して、現在のアプリケーションのSpring設定の完全なビューを提供します。

![]({{ site.url }}/images/jhipster-control-center-configuration.png)

### ***ログ***

ログページでは、実行中のアプリケーションのLogback設定を実行時に管理できます。

Javaパッケージのログ・レベルを変更するには、ボタンをクリックします。これは、開発環境と本番環境の両方で非常に便利です。

![]({{ site.url }}/images/jhipster-control-center-logs.png)

### ***ログファイル***

ログファイルのページでは、実行中のアプリケーションのログを実行時に表示できます。デフォルトでは無効になっているため、設定する必要があります。ログ・ファイルが無効になっている場合は、次のメッセージが表示されます。

```
使用可能なログファイルがありません。デフォルトでは使用できません。以下のSpring Bootプロパティを設定する必要があります。
以下を確認してください。
 - マイクロサービスが起動しているかどうか
 - 以下のプロパティが設定されているかどうか
     - logging.file.path
     - logging.file.name（同じspring.logを使用しないため）

参考:
 - https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html
 - https://docs.spring.io/spring-boot/docs/current/reference/html/howto-logging.html
```

![]({{ site.url }}/images/jhipster-control-center-logfile.png)

### ***API***

APIページでは、アプリケーションのすべてのAPIドキュメントを表示し、単一のSwagger UIフレームを使用してエンドポイントをテストできます。

![]({{ site.url }}/images/jhipster-control-center-api.png)

