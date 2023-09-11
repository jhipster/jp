---
layout: default
title: JHipsterドメイン言語
permalink: /jdl/intro
redirect_from:
  - /jdl/
sitemap:
    priority: 0.5
    lastmod: 2023-07-09T23:00:00-00:00
---

# <i class="fa fa-star"></i> JHipsterドメイン言語(JDL)

JDLはJHipster固有のドメイン言語であり、すべてのアプリケーション、デプロイメント、エンティティ、および
それらの関係を1つのファイル（または複数のファイル）に、使いやすい構文で記述します。

オンライン[JDL-Studio](https://start.jhipster.tech/jdl-studio/)または
[JHipster IDE](https://www.jhipster.tech/jhipster-ide/)プラグイン/拡張機能、以下の開発環境で、JDLファイルの作成とそのUMLのビジュアル化ができます。
  - [IntelliJ](https://plugins.jetbrains.com/plugin/19697-jhipster-jdl)
  - [Eclipse](https://marketplace.eclipse.org/content/jhipster-ide), 
  - [VS Code](https://marketplace.visualstudio.com/items?itemName=jhipster-ide.jdl)

JDLモデルのURLを作成しエクスポートまたは共有もできます。

JDLは、[エンティティ・サブジェネレータ]({{ site.url }}/creating-an-entity/)を使用する代わりとして使用できます。
これは推奨されるアプローチで、
ビジュアルツールを使用して[関係を管理する]({{ site.url }}/managing-relationships/)方がはるかに簡単です。
古典的なYeomanの質問と回答でエンティティを作成する方法よりも優れています。

<<<<<<< HEAD
JDLプロジェクトは[GitHubで利用可能](https://github.com/jhipster/generator-jhipster/tree/main/jdl)であり、
JHipster（Apache 2.0ライセンス）なオープンソースプロジェクトです。JDL構文をパースするためのnodeライブラリとしても使用できます。

_[JHipsterドメイン言語](https://github.com/jhipster/generator-jhipster/tree/main/jdl)が気に入ったら、
[JDL Studio](https://github.com/jhipster/jdl-studio/)または
[JHipster IDE](https://github.com/jhipster/jhipster-ide/)の
[GitHub](https://github.com/jhipster/)にスターを付けるのを忘れないでください - よろしくお願いします_！
=======
The JDL project is [available on GitHub](https://github.com/jhipster/generator-jhipster/), it is an Open Source project like
JHipster (Apache 2.0 License). It can also be used as a node library to do JDL parsing.

_If you like the [JHipster Domain Language](https://github.com/jhipster/generator-jhipster/),
the [JDL Studio](https://github.com/jhipster/jdl-studio/) or the
[JHipster IDE](https://github.com/jhipster/jhipster-ide/) don't forget to give them a star on
[GitHub](https://github.com/jhipster/) - thanks_!
>>>>>>> upstream/main

---

JDLがまだわからない場合は、まず[JHipsterドメイン言語(JDL) - 入門](/jdl/getting-started)ページにアクセスすることをお勧めします。

<<<<<<< HEAD
ただし、すでにJDLに精通していて、JDLを使用して何ができるかを知っている場合は、詳細の参照もできます。
マニュアルは以下です。
  1. [アプリケーション](/jdl/applications)
  1. [エンティティとフィールド](/jdl/entities-fields)
  1. [列挙型](/jdl/enums)
  1. [リレーションシップ](/jdl/relationships)
  1. [オプション](/jdl/options)
  1. [デプロイメント](/jdl/deployments)
  1. [トラブルシューティング](/jdl/troubleshooting)
=======
However, if you're already familiar with the JDL and what you can do with it, you can also browse the detailed
documentation:
  1. [Getting Started](/jdl/getting-started)
  1. [Applications](/jdl/applications)
  1. [Entities & fields](/jdl/entities-fields)
  1. [Enums](/jdl/enums)
  1. [Relationships](/jdl/relationships)
  1. [Options](/jdl/options)
  1. [Deployments](/jdl/deployments)
  1. [Troubleshooting](/jdl/troubleshooting)
>>>>>>> upstream/main

また、公式の[JDLサンプルリポジトリ](https://github.com/jhipster/jdl-samples)でも内容チェックできますし、
あなた方よりサンプルをご提案いただくこともできます！

---

すでに既存のデータベースがあり、JDL表現を作成したい場合は、
このプロジェクト[SQL to JDL](https://github.com/Blackdread/sql-to-jdl)を使用すると、すぐに開始できます。
