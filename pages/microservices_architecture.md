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

* [ゲートウェイ]({{ site.url }}/api-gateway/)は、JHipsterで生成されたアプリケーション（マイクロサービスゲートウェイタイプを使用）であり、Webトラフィックを処理し、Angular、React、またはVueアプリケーションを提供するように設計されています。複数のゲートウェイを使用して[Backends for Frontendsパターン](https://www.thoughtworks.com/insights/blog/bff-soundcloud)に従うことも可能ですが、必須ではありません。ゲートウェイはSpring Cloud Gatewayライブラリ上に構築されており、MVCとWebFluxの両方のフレームワークをサポートしています。
 * [Consul]({{ site.url }}/consul/)は、サービスディスカバリーサービスであり、キー/バリューストアでもあります。
 * [JHipster Registry]({{ site.url }}/jhipster-registry/)は、すべてのアプリケーションが登録し、設定を取得するランタイムアプリケーションです。また、ランタイムモニタリングダッシュボードも提供します。Consulの代替として使用することもできます。*(非推奨)*
 * [マイクロサービス]({{ site.url }}/creating-microservices/)は、JHipsterで生成されたアプリケーションで（生成時に`microservice application`タイプを使用）、RESTリクエストを処理します。これらはステートレスであり、複数のインスタンスを並行して起動することで、重い負荷に対応できます。

この図は、Netflix OSS、Spring Cloud、およびDockerなどの主要技術を組み込んだJHipsterを利用したマイクロサービスアーキテクチャを示しています。Webトラフィックとユーザー認証を処理するゲートウェイ、バックエンド業務を行うマイクロサービス、およびOpenTelemetry、Elasticsearch、Logstash、Kibanaなどのツールを使用した包括的なモニタリングとログ記録が特徴です。

<img src="{{ site.url }}/images/microservices_architecture_updated.png" alt="Diagram" style="width: 930px; height: 558px"/>
