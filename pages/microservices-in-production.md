---
layout: default
title: プロダクション環境下でのマイクロサービス
permalink: /microservices-in-production/
sitemap:
    priority: 0.7
    lastmod: 2020-09-11T00:00:00-00:00
---

# <i class="fa fa-cloud"></i> プロダクション環境下でのマイクロサービス

マイクロサービスは、特定の種類のJHipsterアプリケーションです。プロダクションビルドの実行、最適化、およびセキュリティ保護の詳細については、メインの[プロダクション環境下でのJHipsterのドキュメント]({{ site.url }}/production)を参照してください。

<h2 id="elk">マイクロサービスの監視</h2>

JHipsterレジストリを使用する場合、使用可能なランタイムダッシュボードとその使用方法については、[JHipsterレジストリのドキュメント]({{ site.url }}/jhipster-registry)を参照してください。

[モニタリングのドキュメント]({{ site.url }}/monitoring)も非常に重要であり、以下の使用に関する具体的な情報を得ることができます。

- マイクロサービスのログを収集するELK
- マイクロサービスのメトリクスを収集するPrometheus
- サービス全体のHTTP要求をトレースするZipkin

<h2 id="docker_compose">Docker Composeを使用した開発とデプロイ</h2>

マイクロサービスアーキテクチャで作業するということは、複数の異なるサービスとデータベースを連携させる必要があるということであり、その意味でDocker Composeは、開発、テスト、運用環境を管理するための優れたツールです。

マイクロサービスに関する特定のセクションは、[Docker Composeドキュメント]({{ site.url }}/docker-compose#microservices)に含まれており、マイクロサービスアーキテクチャに取り組む際には、このセクションに精通することを強くお勧めします。

Docker SwarmはDocker Machineと同じAPIを使用しているため、クラウドにマイクロサービスアーキテクチャをデプロイすることは、ローカルマシンにデプロイすることとまったく同じです。JHipsterでDocker Composeを使用する方法の詳細については、[Docker Composeドキュメント]({{ site.url }}/docker-compose/)に従ってください。

<h2 id="cloudfoundry">Cloud Foundryによる本番環境への移行</h2>

[Cloud Foundryサブジェネレータ]({{ site.url }}/cloudfoundry/)は、マイクロサービスアーキテクチャでも同じように動作しますが、主な違いは、デプロイするアプリケーションがより多いことです。

- [Cloud Foundryサブジェネレータ]({{ site.url }}/cloudfoundry/)を使用して、最初にJHipsterレジストリ（通常のJHipsterアプリケーション）をデプロイします。
- JHipsterレジストリがデプロイされているURLをメモします。アプリケーションはすべてそのURLを指している必要があります。
  - `bootstrap-prod.yml`ファイルでは、`spring.cloud.config.uri`は`http(s)://<your_jhipster_registry_url>/config/`を指している必要があります。
  - `application-prod.yml`ファイルでは、`eureka.client.serviceUrl.defaultZone`は`http(s)://<your_jhipster_registry_url>/eureka/`を指している必要があります。
- ゲートウェイとマイクロサービスをデプロイします。
- Cloud Foundryを使用して、アプリケーションを通常どおりにスケールアップします。

覚えておくべき重要な点の1つは、JHipsterレジストリはデフォルトでは保護されておらず、マイクロサービスは外部からアクセスできないことになっていることです。ユーザはゲートウェイを使用してアプリケーションにアクセスすることになります。

この問題を解決するには、次の2つの方法があります。

- 特定のルートを使用してCloud Foundryを保護します。
- すべてを公開したまま、すべての場所でHTTPSを使用し、Spring Securityの基本認証サポートを使用してJHipsterレジストリを保護します。

<h2 id="heroku">Herokuを使用した本番環境への移行</h2>

[Herokuサブジェネレータ]({{ site.url }}/heroku/)は、マイクロサービスアーキテクチャとほぼ同じように動作しますが、主な違いは、デプロイするアプリケーションがより多いことです。

ワンクリックでJHipsterレジストリを直接デプロイします。

[![Herokuへのデプロイ](https://camo.githubusercontent.com/c0824806f5221ebb7d25e559568582dd39dd1170/68747470733a2f2f7777772e6865726f6b7563646e2e636f6d2f6465706c6f792f627574746f6e2e706e67)](https://dashboard.heroku.com/new?&template=https%3A%2F%2Fgithub.com%2Fjhipster%2Fjhipster-registry)

JHipsterレジストリをセキュアにする方法を理解するには、[Herokuサブジェネレータのドキュメント]({{ site.url }}/heroku/)に従ってください。

JHipsterレジストリがデプロイされているURLをメモします。アプリケーションはすべて、`application-prod.yml`ファイルでそのURLを指定する必要があります。その構成を次のように変更します。

    eureka:
        instance:
            hostname: https://admin:[password]@[appname].herokuapp.com
            prefer-ip-address: false

これで、ゲートウェイとマイクロサービスをデプロイし、スケールができます。Herokuのサブジェネレータは、JHipsterレジストリのURLを知るために、新しい質問をします。これにより、アプリケーションはSpring Cloud Configサーバで設定を取得できるようになります。
