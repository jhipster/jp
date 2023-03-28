---
layout: default
title: Couchbaseの使用
permalink: /using-couchbase/
redirect_from:
  - /using_couchbase.html
sitemap:
    priority: 0.7
    lastmod: 2015-02-24T00:00:00-00:00
---

# <i class="fa fa-database"></i> Couchbaseの使用

Couchbaseはサポートされているデータベースの1つで、アプリケーションの生成時に選択できます。

Couchbaseを選択した場合、以下のとおりとなります。

* データベースへのアクセスにはSpring Data Couchbaseが使用されます。これはSpring Data JPAに非常に近いものであり、Couchbaseサポートが（デフォルトの）JPAサポートに非常に近いのはこのためです。
* データベースの変更管理のために[Couchmove](https://github.com/differentway/couchmove)が[Liquibase](http://www.liquibase.org/)の代わりに使用されます。
* [エンティティサブジェネレータ]({{ site.url }}/creating-an-entity/)は、NoSQLデータベースとのリレーションシップを持つことができない（少なくともJPAでリレーションシップを持つ方法ではない）ため、エンティティのリレーションシップを要求しません。
* [Couchbase Testcontainers](https://github.com/differentway/testcontainers-java-module-couchbase)は、ユニット・テストを実行するためのコンテナ化されたバージョンのデータベースを起動するために使用されます。

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
