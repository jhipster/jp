---
layout: default
title: Neo4jの使用
permalink: /using-neo4j/
redirect_from:
  - /using_neo4j.html
sitemap:
    priority: 0.7
    lastmod: 2020-01-18T00:00:00-00:00
---

# <i class="fa fa-database"></i> Neo4jの使用 [BETA]

[Neo4j](https://neo4j.com/)は、サポートされているデータベースの1つで、アプリケーションの生成時に選択できます。

Neo4jが選択されている場合。

* [Spring Data Neo4j/RX](https://neo4j.github.io/sdn-rx)は、データベースへのアクセスに使用されます。これはSpring Data JPAに非常に近いものであり、Neo4jのサポートは（デフォルトの）JPAサポートに非常に近いのはこのためです。
* データベースの変更管理のために、[Liquibase](http://www.liquibase.org/)の代わりに[Neo4j Migrations](https://github.com/michael-simons/neo4j-migrations)が使用されます。
* [Neo4j Testcontainers](https://www.testcontainers.org/modules/databases/neo4j/)は、ユニット・テストを実行するためのコンテナ化されたバージョンのデータベースを起動するために使用されます。

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
