---
layout: default
title: MongoDBの使用
permalink: /using-mongodb/
redirect_from:
  - /using_mongodb.html
sitemap:
    priority: 0.7
    lastmod: 2015-02-24T00:00:00-00:00
---

# <i class="fa fa-leaf"></i> MongoDBの使用

MongoDBはサポートされているデータベースのひとつで、アプリケーションの生成時に選択できます。

MongoDBが選択された場合、以下のようになります。

*   データベースへのアクセスにはSpring Data MongoDBが使用されます。これはSpring Data JPAに非常に近いものであり、MongoDBサポートが（デフォルトの）JPAサポートに非常に近いのはこのためです。
*   データベースの変更管理のために[Mongock](https://www.mongock.io)が[Liquibase](http://www.liquibase.org/)の代わりに使用されます。
*   [de.flapdoodle.embed.mongo](https://github.com/flapdoodle-oss/de.flapdoodle.embed.mongo)は、ユニットテストを実行するためのインメモリバージョンのデータベースを実行するために使用されます。


<br/><br/><br/><br/><br/>