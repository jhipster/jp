---
layout: default
title: Elasticsearchの使用
permalink: /using-elasticsearch/
redirect_from:
  - /using_elasticsearch.html
sitemap:
    priority: 0.7
    lastmod: 2023-07-12T00:00:00-00:00
---

# <i class="fa fa-search"></i> Elasticsearchの使用

Elasticsearchは、データベースの上に検索機能を追加するオプションです。

このオプションにはいくつかの制限があります。

* SQLデータベースとMongoDBでのみ動作します。CassandraとCouchbaseのサポートは将来追加される予定です（ヘルプは歓迎です！）。
* データベースとElasticsearchの間には自動レプリケーションメカニズムがないため、データが同期していない可能性があります。その結果、データを同期するための特定のコードを記述する必要があります。たとえば、Springの`@Scheduled`アノテーションを使用して、毎晩実行する必要があります。
    * これはまた、データベースがアプリケーションの外部で変更された場合、検索インデックスが同期しなくなることを意味します。[Elasticsearch Reindexer](https://www.jhipster.tech/modules/marketplace/#/details/generator-jhipster-elasticsearch-reindexer)JHipsterモジュールは、このような状況で役立ちます。

Elasticsearchオプションが選択されている場合、以下のふるまいとなります。

*   Spring Data Elasticsearchは、Spring Bootの自動設定で使用されます。これは`spring.elasticsearch.*`設定プロパティを使用して設定できます。
*   "repository"パッケージには、すべてのElasticsearchリポジトリを保持する"search"と呼ばれる新しいサブパッケージができます。
*   "User"エンティティはElasticsearchでインデックス付けされ、`/api/_search/users/:query`RESTエンドポイントを使用してクエリできます。
*   [エンティティサブジェネレータ]({{ site.url }}/creating-an-entity/)を使用すると、生成されたエンティティはElasticsearchによって自動的にインデックス付けされ、RESTエンドポイントで使用されます。UIには検索機能も追加されているため、CRUDのメイン画面でエンティティを検索できます。

### 開発環境での使用


開発環境では、JHipsterは組み込みのElasticsearchインスタンスで実行されます。`SPRING_DATA_URIS`環境変数を設定すれば（または`spring.elasticsearch.uris`プロパティを`application-dev.yml`に追加すれば）、外部のElasticsearchインスタンスを使用することもできます。

    docker-compose -f src/main/docker/elasticsearch.yml up -d
    
デフォルトでは、`SPRING_ELASTICSEARCH_URIS`プロパティは`application-dev.yml`および`application-prod.yml`内で、このインスタンスと通信するように設定されています。

次に、それを指す環境変数を設定します。

    export SPRING_DATA_URIS=http://localhost:9200

### 本番環境での使用

本番環境では、JHipsterは外部Elasticsearchインスタンスを想定しています。デフォルトでは、アプリケーションはlocalhostで実行されているElasticsearchインスタンスを検索します。これは、`application-prod.yml`ファイルの標準のSpring Bootプロパティを使用して設定できます。

### Herokuでの使用

Herokuでは、[Bonsai Elasticsearch](https://elements.heroku.com/addons/bonsai)はアドオンとして設定されています。JHipsterは自動的にそれと通信するように設定されます。

残念ながら、JHipster 7.9.3の時点で、Elasticsearchは[Herokuではそのままでは動作しません](https://github.com/jhipster/generator-jhipster/issues/20315)。これを解決するには、ElasticsearchでDockerイメージを作成して、それを実行できる場所にデプロイするか、Elastic Cloudを使用することになります。[Elasticsearch Add-on](https://elements.heroku.com/addons/foundelasticsearch)は、最も安いプランが月67米ドルで少し高いように思われるため、自動的な設定は行いません。

### Elastic Cloudの使用

Elastic Cloudで[フリートライアルを始める](https://cloud.elastic.co/registration) ことが可能です。ログインしたらデプロイメントを作成します。デフォルト設定を使用して、バージョンとして**7.17.7**を選択し、**Create deployment**を押します。

**警告**：最新バージョンを使用すると"Unable to parse response body"エラーが発生します。

次の画面から認証情報をダウンロードし、**Continue**をクリックします。次に、メニューから**Manage this deployment**を選択し、Elasticsearchエンドポイントをコピーします。

認証情報とエンドポイントURLをHerokuの新しい`ELASTIC_URL`環境変数として設定してください。

```shell
heroku config:set ELASTIC_URL=https://elastic:<password>@<endpoint-url>
```

次に、`heroku.gradle`を変更してBonsai（動作しなくなりました）の回避策を削除し、`application-heroku.yml`を更新して`ELASTIC_URL`を使用します。

```yaml
spring:
  ...
  elasticsearch:
    uris: ${ELASTIC_URL}
```

アプリケーションをHerokuに再デプロイすれば、すべてが期待通りに動作するはずです。
