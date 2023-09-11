---
layout: default
title: マイクロサービスの構築
permalink: /creating-microservices/
sitemap:
    priority: 0.7
    lastmod: 2017-05-03T00:00:00-00:00
---

# <i class="fa fa-bolt"></i> マイクロサービスの構築

<<<<<<< HEAD
マイクロサービスはJHipsterアプリケーションの一種であり、フロントエンドを持たず（Angularフロントエンドは[gateway]({{ site.url }}/api-gateway/)で生成される必要があります）、[JHipsterレジストリ]({{ site.url }}/jhipster-registry/)と連携して設定、検出、管理されます。
=======
Microservices are a type of JHipster application, that have no front-end (the Angular front-end must be generated on a [gateway]({{ site.url }}/api-gateway/)), and which work with the [Consul]({{ site.url }}/consul/) to be configured, discovered, and managed.
>>>>>>> upstream/main

<h2 id="entities">マイクロサービスアーキテクチャにおけるエンティティ</h2>

JWTまたはDTOを使用する場合、Userエンティティはマイクロサービスで生成されません。OAuth 2.0が使用される場合、マイクロサービスには、トークンからユーザーデータを抽出し、それをマイクロサービスのデータベースに保存するメカニズムがあります。そのため、JWTおよびDTOの場合、Userエンティティはゲートウェイのデータベースにのみ存在するため、Userエンティティとの関係を使用または定義できません。

異なるマイクロサービスのエンティティ間の関係はサポートされていません。

<h2 id="generating_entities">エンティティの生成</h2>

マイクロフロントエンドのエンティティについては、[マイクロフロントエンド](#microfrontends)を参照してください。

[エンティティサブジェネレータ]({{ site.url }}/creating-an-entity/)を使用すると、フロントエンドとバックエンドのコードが同じアプリケーションに配置されないため、マイクロサービスアーキテクチャでの動作が少し異なります。

まず、マイクロサービスアプリケーションでエンティティを生成します。これは通常どおりに動作し、[JHipster UML]({{ site.url }}/jhipster-uml/)または[JDL Studio](https://start.jhipster.tech/jdl-studio/)を使用して、複雑なエンティティとリレーションシップも生成できます。マイクロサービスにはフロントエンドがないため、UIコードは生成されません。

次に、ゲートウェイでエンティティサブジェネレータを再度実行します。最初に、ゲートウェイに固有の新しい質問が表示されます。

- 新しいエンティティを通常生成するか（ゲートウェイも標準のJHipsterアプリケーションなので、これはモノリスアプリケーションのように動作します）、マイクロサービスから既存のJHipster構成を使用するかを選択できます。
- マイクロサービスからエンティティを生成することを選択した場合、ローカルコンピュータ上のこのマイクロサービスへのパスを入力する必要があります。すると、JHipsterがゲートウェイ上にフロントエンドコードを生成します。

## マイクロフロントエンド

Microfrontendサポートは進行中です。実装は変更される可能性があり、フレームワークによって異なります。最新のステータスについては、[マイクロフロントエンドのサポート](https://github.com/jhipster/generator-jhipster/issues/17031)を参照してください。

<<<<<<< HEAD
JHipsterのマイクロフロントエンド実装は、[Webpack Module Federaration](https://webpack.js.org/concepts/module-federation/)を使用し、フロントエンドエンティティの実装をゲートウェイではなくマイクロサービスに配置できるようにします。
=======
JHipster's microfrontends implementation uses [Webpack Module Federation](https://webpack.js.org/concepts/module-federation/) and allows frontend entities implementation to be located in the microservice instead of in the gateway.
>>>>>>> upstream/main

開発段階では、認証プロセスのためにゲートウェイを実行する必要があります。

ゲートウェイを使用して、または単独でマイクロフロントエンドを起動する方法については、生成されたREADMEを参照してください。

<h2 id="hazelcast">Hazelcastによる分散キャッシュ</h2>

アプリケーションでSQLデータベースを使用している場合、JHipsterはマイクロサービスを使用した異なる第2レベルのキャッシュソリューションを提案しています。

- マイクロサービスを備えたJHipsterのデフォルトのキャッシュソリューションはHazelcastです。
- Ehcache（モノリスアプリケーションのデフォルトソリューション）またはCaffeineを選択するか、キャッシュをまったく使用しないことも選択できます。

このアーキテクチャでは、サービスを拡張するという考え方であるため、このソリューションはマイクロサービスのデフォルトです。

- ローカルキャッシュを使用すると、サービスインスタンスに同期化されたキャッシュがないため、誤ったデータが生成されることになります。
- キャッシュがないと、スケーリングの負担がデータベースに押し込まれ、（Cassandraオプションを使用しない限り）あまりうまくいきません。

マイクロサービスでHazelcastを使用すると、特定の構成となります。

<<<<<<< HEAD
- 起動時に、アプリケーションはJHipsterレジストリに接続して、同じサービスの他のインスタンスが実行されているかどうかを確認します。
- `dev`プロファイルを使用すると、JHipsterはインスタンスごとに異なるポートを使用して、localhost(`127.0.0.1`)にこれらのインスタンスのクラスタを作成します。デフォルトでは、Hazelcastポートは`アプリケーションのポート+5701`です（したがって、アプリケーションのポートが`8081`の場合、Hazelcastはポート`13782`を使用します）。
- `prod`プロファイルを使用すると、JHipsterはデフォルトのHazelcastポート（`5701`）を使用して、検出した他のすべてのノードとともにクラスタを作成します。
=======
- At start-up, your application will connect to the Service Registry to find if other instances of the same service are running
- With the `dev` profile, JHipster will create a cluster of those instances on localhost (`127.0.0.1`),  using a different port per instance. By default, the Hazelcast port is `your application's port + 5701` (so if your application's port is `8081`, Hazelcast will use port `13782`)
- With the `prod` profile, JHipster will create a cluster with all the other nodes it finds, using the default Hazelcast port (`5701`)
>>>>>>> upstream/main

<h2 id="no_database">データベースを持たないマイクロサービス</h2>

データベースなしで作成できるのはマイクロサービスアプリケーションだけです。これは、マイクロサービスが小さく、ユーザ管理コードがないためです。

データベースのないマイクロサービスは非常に小さく、レガシーシステムのような特定のバックエンドに接続するために使用されます。
