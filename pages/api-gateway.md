---
layout: default
title: APIゲートウェイ
permalink: /api-gateway/
sitemap:
    priority: 0.7
    lastmod: 2024-06-03T00:00:00-00:00
---

# <i class="fa fa-exchange"></i> JHipster APIゲートウェイ

JHipsterはAPIゲートウェイを生成できます。ゲートウェイは通常のJHipsterアプリケーションであるため、そのプロジェクトでは通常のJHipsterオプションと開発ワークフローを使用できますが、マイクロサービスへの入り口としても機能します。より具体的には、HTTPルーティングとロードバランシング、サービス品質、セキュリティ、およびすべてのマイクロサービスのAPIドキュメントを提供します。

## サマリー

1. [アーキテクチャ図](#architecture_diagram)
2. [HTTPルーティング](#http_routing)
3. [セキュリティ](#security)
4. [自動ドキュメンテーション](#documentation)
5. [レート制限](#rate_limiting)
6. [アクセス制御ポリシー](#acl)

<h2 id="architecture_diagram">アーキテクチャ図</h2>

<img src="{{ site.url }}/images/microservices_architecture_detail.006.png" alt="Diagram" style="width: 800; height: 600" class="img-responsive"/>

<h2 id="http_routing">ゲートウェイを使用したHTTPリクエストのルーティング</h2>

ゲートウェイとマイクロサービスが起動されると、自身をConsulサービスレジストリに登録します。

ゲートウェイは、アプリケーション名を使用して、すべてのリクエストをマイクロサービスに自動的にプロキシします。たとえば、マイクロサービス`app1`が登録されている場合、ゲートウェイの`/services/app1`のURLで利用できます。

<<<<<<< HEAD
たとえば、ゲートウェイが`localhost:8080`で実行されている場合、[http://localhost:8080/services/app1/api/foos](http://localhost:8080/services/app1/api/foos)の指定で、
マイクロサービス`app1`で提供されている`foos`のリソースを取得できます。Webブラウザでこれを行おうとしている場合は、RESTリソースがJHipsterでデフォルトで保護されていることを忘れないでください。したがって、正しいJWTヘッダーを送信するか（以下のセキュリティのポイントを参照）、以降のセキュリティに関するポイントを確認するか、またはマイクロサービスの`MicroserviceSecurityConfiguration`クラスでそれらのURLのセキュリティを削除する必要があります。

同じサービスのインスタンスが複数実行されている場合、ゲートウェイはそれらのインスタンスをJHipsterレジストリから取得し、[Consul](https://www.consul.io/use-cases/load-balancing)を使用してHTTPリクエストのロードバランシングを行います。
=======
For example, if your gateway is running on `localhost:8080`, you could point to [http://localhost:8080/services/app1/api/foos](http://localhost:8080/services/app1/api/foos) to
get the `foos` resource served by microservice `app1`. If you're trying to do this with your Web browser, don't forget REST resources are secured by default in JHipster, so you need to send the correct JWT header (see the point on security below), or remove the security on those URLs in the microservice's `SecurityConfiguration` class.

If several instances of the same service are running, the gateway will get those instances from the Service Registry and load balance HTTP requests using [Consul](https://www.consul.io/use-cases/load-balancing). You can access a detailed list of running microservices, including their IP addresses, Git version, status, and more, at [http://localhost:8080/api/gateway/routes](http://localhost:8080/api/gateway/routes). This endpoint is secured for protection.
>>>>>>> upstream/main

各ゲートウェイには特定の"admin > gateway"メニューがあり、オープンされたHTTPルートとマイクロサービスインスタンスを監視できます。

<h2 id="security">セキュリティ</h2>

標準のJHipsterセキュリティオプションについては、[このセキュリティドキュメントページ]({{ site.url }}/security/)で詳しく説明されています。ただし、マイクロサービスアーキテクチャのセキュリティ保護には、いくつかの特定のチューニングとオプションがあります。これらについては、ここで詳しく説明します。

### JWT (JSON Web Token)

JWT (JSON Web Token)は、マイクロサービスアーキテクチャでアプリケーションを保護するための、業界標準の使いやすい方法です。

JHipsterは、Okta社が提供する[JJWTライブラリ](https://github.com/jwtk/jjwt)のJWT実装を使用します。

トークンはゲートウェイによって生成され、基盤となるマイクロサービスに送信されます。共通のシークレットキーを共有するため、マイクロサービスはトークンを検証し、そのトークンを使用するユーザを認証できます。

これらのトークンは自己充足的であり、認証情報と認可情報の両方を持っているため、マイクロサービスはデータベースや外部システムに問い合わせる必要がありません。これは、スケーラブルなアーキテクチャを確保するために重要です。

セキュリティーを機能させるためには、JWTのシークレットトークンをすべてのアプリケーションで共有する必要があります。

- 各アプリケーションのデフォルトトークンは固有であり、JHipsterによって生成されます。これは`.yo-rc.json`ファイルに格納されます。
- トークンは、`src/main/resources/config/application.yml`ファイル内の`jhipster.security.authentication.jwt.secret`キーで構成されます。
- このキーをすべてのアプリケーション間で共有するには、ゲートウェイからすべてのマイクロサービスにキーをコピーするか、[JHipster固有のConsul K/Vストアの設定]({{ site.url }}/consul/)を使用してキーを共有します。これが、中央構成サーバが使用される主な理由の1つです。
- 開発と本番で異なるキーを使用することをお勧めします。

### OpenID Connect

JHipsterはOpenID Connectのサポートを提供しており、詳細は[OpenID Connectのドキュメント]({{ site.url }}/security/#oauth2)に記載されています。

このオプションを選択すると、デフォルトでKeycloakが使用され、Docker Composeを使用して完全なマイクロサービスアーキテクチャを実行することになります。[Docker Composeドキュメント]({{ site.url }}/docker-compose/)を必ず読み、Keycloak用に`/etc/hosts`を正しく設定してください。

OpenID Connectを使用する場合、JHipsterゲートウェイはOAuth2トークンをマイクロサービスに送信し、マイクロサービスはKeycloakにも接続されているトークンを受け入れます。

JWTとは異なり、これらのトークンは自己充足的ではなく、ステートフルである必要があるため、次のような問題が発生します。

- マイクロサービスのパフォーマンスの問題：現在のユーザのセキュリティ情報を探すことは非常に一般的なため（そうでなければ最初からセキュリティオプションを使用することはありません）、各マイクロサービスはOpenID Connectサーバを呼び出してデータを取得します。そのため、通常のセットアップでは、これらの呼び出しは、リクエストを受け取るたびに各マイクロサービスによって行われ、これはすぐにパフォーマンスの問題を引き起こします。
  - JHipsterマイクロサービスを生成するときに、キャッシュオプション（[「キャッシュの使用」のドキュメントを参照]({{ site.url }}/using-cache/)）を選択した場合、これらの呼び出しをキャッシュする固有の`CachedUserInfoTokenServices`Spring Beanが生成されます。適切にチューニングされれば、パフォーマンスの問題は解消されます。
  - この「ユーザー情報」リクエストに関する詳細が必要な場合は、`src/main/resources/application.yml`構成ファイル内の標準のSpring Boot構成キー`security.oauth2.resource.userInfoUri`を使用して構成されます。

<h2 id="documentation">自動ドキュメンテーション</h2>

ゲートウェイは、proxifiesのサービスのSwagger API定義を公開するため、Swagger UIやswagger-codegenなどのすべての有用なツールの恩恵を受けることができます。

ゲートウェイの「admin>API」メニューには、ゲートウェイのAPIと登録されたマイクロサービスのすべてのAPIを示す、固有のドロップダウンリストがあります。

このドロップダウンリストを使用すると、すべてのマイクロサービスAPIが自動的に文書化され、ゲートウェイからテスト可能になります。

セキュアなAPIを使用すると、セキュリティトークンがSwagger UIインタフェースに自動的に追加されるため、すべてのリクエストがすぐに機能するようになります。

<h2 id="rate_limiting">レート制限</h2>

これは、[Bucket4j](https://github.com/vladimir-bukhtoyarov/bucket4j)と[Hazelcast](https://hazelcast.com/)を使用して、マイクロサービスのQoSを提供する高度な機能です。

ゲートウェイはレート制限機能を提供するため、RESTリクエストの数を制限できます。

- IPアドレスによる制限（匿名ユーザの場合）
- ユーザログインによる制限（ログインユーザの場合）

JHipsterは、[Bucket4j](https://github.com/vladimir-bukhtoyarov/bucket4j)と[Hazelcast](https://hazelcast.com/)を使用してリクエスト数を計算し、制限を超えた場合にHTTP 429（過大なリクエストが発生）エラーを送信します。ユーザごとのデフォルトの制限は、1時間あたり100,000 APIコールです。

これは、特定のユーザのリクエストの洪水からマイクロサービスアーキテクチャを保護するための重要な機能です。

ゲートウェイはRESTエンドポイントを保護するため、ユーザのセキュリティ情報に完全にアクセスできるので、ユーザのセキュリティロールに応じて特定のレート制限を提供するように拡張できます。

レート制限を有効にするには、`application-dev.yml`または`application-prod.yml`ファイルを開き、`enabled`を`true`に設定します。

    jhipster:
        gateway:
            rate-limiting:
                enabled: true

データはHazelcastに格納されるため、Hazelcast分散キャッシュが設定されていれば、ゲートウェイの拡張が可能であり、すぐに動作するはずです。

- すべてのゲートウェイには、デフォルトでHazelcastが設定されています。

さらにルールを追加する場合、または既存のルールを変更する場合は、それらを`RateLimitingFilter`クラスでコーディングする必要があります。変更の例は次のとおりです。

- HTTP呼び出しの制限を下げる
- 1分または1日あたりの制限を追加
- "admin"ユーザーの制限をすべて削除

<h2 id="acl">アクセス制御ポリシー</h2>

デフォルトでは、登録されたすべてのマイクロサービスがゲートウェイを通じて利用可能です。ゲートウェイを通じて公開される特定のAPIを除外する場合は、ゲートウェイ固有のアクセス制御ポリシーフィルタを使用できます。これは、`application-*.yml`ファイルの`jhipster.gateway.authorized-microservices-endpoints`キーを使うことで設定可能です。

    jhipster:
        gateway:
            authorized-microservices-endpoints: # アクセス制御ポリシー。ルートに対して空のままにすると、すべてのエンドポイントがアクセス可能になります。
                app1: /api,/v2/api-docs # 開発時の推奨設定

たとえば、マイクロサービス`bar`の`/api/foo`エンドポイントのみを使用可能にする場合は、次のように入力します。

    jhipster:
        gateway:
            authorized-microservices-endpoints:
                bar: /api/foo
<h2 id="acl">Enabling TLS for Gateway Security </h2>
By default, the gateway operates over unsecured HTTP. For production environments, it's recommended to enable TLS for enhanced security. To do this, uncomment the provided code snippet, under `application-prod.yml`. This will utilize a self-signed TLS certificate located in `config/tls` with the filename `keystore.p12`, or you can specify your own keystore with a predefined password.

	server:
	   port: 443
   		ssl:
		   key-store: classpath:config/tls/keystore.p12
	       key-store-password: password
   		   key-store-type: PKCS12
           key-alias: selfsigned
          # The ciphers suite enforce the security by deactivating some old and deprecated SSL cipher, this list was tested against SSL Labs (https://www.ssllabs.com/ssltest/)
	       ciphers: TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 ,TLS_DHE_RSA_WITH_AES_128_GCM_SHA256 ,TLS_DHE_RSA_WITH_AES_256_GCM_SHA384 ,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384,TLS_DHE_RSA_WITH_AES_128_CBC_SHA256,TLS_DHE_RSA_WITH_AES_128_CBC_SHA,TLS_DHE_RSA_WITH_AES_256_CBC_SHA256,TLS_DHE_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_128_GCM_SHA256,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_CBC_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA256,TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA,TLS_RSA_WITH_CAMELLIA_256_CBC_SHA,TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA,TLS_RSA_WITH_CAMELLIA_128_CBC_SHA

Keep in mind that enabling TLS on the server might introduce some performance overhead. If possible, consider using a load balancer outside the gateway with SSL termination to handle encryption, which can help mitigate this performance impact.