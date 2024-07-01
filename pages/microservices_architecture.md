---
layout: default
title: JHipsterでマイクロサービスを実行する
permalink: /microservices-architecture/
sitemap:
    priority: 0.7
    lastmod: 2021-03-08T12:00:00-00:00
---

# <i class="fa fa-sitemap"></i> JHipsterでマイクロサービスを実行する

<h2 id="microservices_vs_monolithic">マイクロサービスvsモノリシックアーキテクチャ</h2>

JHipsterが最初に尋ねる質問は、生成するアプリケーションの種類です。次の2つのアーキテクチャスタイルから選択できます。

- 「モノリシック」アーキテクチャは、フロントエンドコードとバックエンドのSpring Bootコードの両方を含む、単一の汎用アプリケーションを使用します。
- 「マイクロサービス」アーキテクチャはフロントエンドとバックエンドを分割するため、アプリケーションのスケーリングとインフラストラクチャの問題への対応が容易になります。

「モノリシック」アプリケーションの方が作業がはるかに簡単なので、特定の要件がない場合は、これがお勧めのオプションであり、デフォルトのオプションです。

<h2 id="overview">マイクロサービスアーキテクチャの概要</h2>

JHipsterのマイクロサービスアーキテクチャは次のように動作します。

<<<<<<< HEAD
* [ゲートウェイ]({{ site.url }}/api-gateway/)は、JHipsterにより生成されるアプリケーションです（生成時にアプリケーションタイプ`microservice gateway`を使用します）。Webトラフィックを処理し、Angular/React/VueJsアプリケーションを提供します。もし[Backends for Frontendsパターン](https://www.thoughtworks.com/insights/blog/bff-soundcloud)に従いたい場合は、複数の異なるゲートウェイを用意できますが、必須ではありません。
* [Consul]({{ site.url }}/consul/)は、サービスディスカバリサービスであり、キー/値ストアでもあります。
* [JHipsterレジストリ]({{ site.url }}/jhipster-registry/)は、すべてのアプリケーションが登録され、その構成を取得するランタイム・アプリケーションです。また、ランタイム監視ダッシュボードも提供します。Conrulの代替として使用できます。
* [マイクロサービス]({{ site.url }}/creating-microservices/)は、JHipsterによって生成されたアプリケーションです（生成時にアプリケーションタイプ`microservice application`を使用します）。RESTリクエストを処理します。ステートレスであり、高い負荷を処理するために複数のインスタンスを並行して起動できます。

次の図では、緑のコンポーネントはアプリケーションに固有のもので、青のコンポーネントはその基盤となるインフラストラクチャを提供します。
=======
* A [gateway]({{ site.url }}/api-gateway/) is a JHipster-generated application (using the microservice gateway type) designed to handle web traffic and serve an Angular, React, or Vue application. While you can have multiple gateways following the [Backends for Frontends pattern](https://www.thoughtworks.com/insights/blog/bff-soundcloud), it's not required. The gateway is built on the Spring Cloud Gateway library and supports both MVC and WebFlux frameworks.
 * [Consul]({{ site.url }}/consul/) is a service discovery service, as well as a key/value store.
 * The [JHipster Registry]({{ site.url }}/jhipster-registry/) is a runtime application on which all applications registers and get their configuration from. It also provides runtime monitoring dashboards. It can be used as an alternative to Consul. *(deprecated)*
 * [Microservices]({{ site.url }}/creating-microservices/) are JHipster-generated applications (using application type `microservice application` when you generate them), that handle REST requests. They are stateless, and several instances of them can be launched in parallel to handle heavy loads.

This diagram illustrates a microservices architecture utilizing JHipster, incorporating key technologies such as Netflix OSS, Spring Cloud, and Docker. It features a gateway for handling web traffic and user authentication, microservices for backend operations, and comprehensive monitoring and logging with tools like OpenTelemetry, Elasticsearch, Logstash, and Kibana.
>>>>>>> upstream/main

<img src="{{ site.url }}/images/microservices_architecture_updated.png" alt="Diagram" style="width: 930px; height: 558px"/>
