---
layout: default
title: Cloud Foundryへのデプロイ
permalink: /cloudfoundry/
redirect_from:
  - /cloudfoundry.html
sitemap:
    priority: 0.7
    lastmod: 2014-11-04T00:00:00-00:00
---

# Cloud Foundryへのデプロイ

このサブジェネレータを使用すると、JHipsterアプリケーションを[Cloud Foundry PaaS](http://cloudfoundry.org/)に自動的にデプロイできます。

MySQL、PostgreSQL、MongoDBクラウドプロバイダで動作します。

## サポートされるクラウド

[![]({{ site.url }}/images/logo/logo-pws.png)](http://run.pivotal.io/)

このサブジェネレータはCloud Foundryコマンドラインツールを使用しており、すべてのCloud Foundryインスタンスにデプロイできます。

*   [Pivotal Web Services](http://run.pivotal.io/)は公式にJHipsterを後援しており、私たちが唯一テストやサポートを提供できるものです。
*   [Atos Canopy](https://canopy-cloud.com/)
*   [IBM Bluemix](https://console.ng.bluemix.net/)
*   また、Cloud Foundryを自分でインストールすることにした場合は、自分専用のCloud Foundryインスタンスを用意します！

## サブジェネレータの実行

サブジェネレータを実行する前に、[cf Command Line Interface (CLI)](http://docs.cloudfoundry.org/devguide/installcf/)をインストールし、Cloud Foundryアカウントを作成する必要があります。

アプリケーションをCloud Foundryにデプロイするには、次のように入力します。

`jhipster cloudfoundry`

データベースを設定するには、データベースサービスの名前と使用するプランを尋ねるいくつかの質問があります。使用可能なデータベースは、現在インストールされているCloud Foundryによって異なります。`cf marketplace`と入力すると、Cloud Foundryマーケットプレイスで使用可能なサービスとプランがわかります。デフォルトでは、JHipsterのスポンサーであることから、パブリックなPivotal Cloud Foundryインスタンス上でElephantSQLの無償PostgreSQLサービスがデータベースとプランとして選択されます。

これにより、アプリケーションが（プロダクションモードまたは開発モードで）パッケージ化され、Cloud Foundryアプリケーションが（データベースとともに）作成され、コードがアップロードされ、アプリケーションが起動します。

## デプロイしたアプリケーションを更新する

アプリケーションがすでにデプロイされている場合は、次のコマンドを実行して通常どおりに構築することで、再デプロイできます。

**Mavenの場合:**

`./mvnw -Pprod package`

`cf push -f ./deploy/cloudfoundry/manifest.yml -p target/*.jar`

**Gradleの場合:**

`./gradlew -Pprod bootJar`

`cf push -f ./deploy/cloudfoundry/manifest.yml -p build/libs/*.jar`

別の機会に次のように入力して、サブジェネレータを再度実行できます。

`jhipster cloudfoundry`

## 詳細情報

*   [Spring Boot Cloud Foundryドキュメント](http://docs.spring.io/spring-boot/docs/current/reference/html/cloud-deployment.html)
*   [Spring Cloudコネクタ](http://cloud.spring.io/spring-cloud-connectors/)
