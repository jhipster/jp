---
layout: default
title: JHipsterドメイン言語 - トラブルシューティング
permalink: /jdl/troubleshooting
sitemap:
    priority: 0.5
    lastmod: 2019-10-27T12:00:00-00:00
---

# <i class="fa fa-star"></i> JHipsterドメイン言語(JDL)

## トラブルシューティング

私たちは、開発者にとって構文をできるだけ使いやすいものにするよう努めました。
これにより、次のことが可能になります。
  - オプションとエンティティを使用してアプリケーションを宣言します。
  - エンティティをその属性とともに宣言します。
  - それらの間のリレーションシップを宣言します。
  - JHipster固有のオプションをいくつか宣言します。

JDLの文法は
[こちら](https://github.com/jhipster/jhipster-core/blob/master/lib/dsl/gen/grammar.html)で見ることができます。

---

### マイクロサービスのbaseNameとエンティティ名が一致する場合、JDLインポートで1つのエンティティしか検出されない

これは、構文解析システムに関する既知の問題であり、修正は困難です。
回避策は、マイクロサービスと内部のエンティティに異なる名前を使用することです。

詳細については、[JHipster Core issue#308](https://github.com/jhipster/jhipster-core/issues/308)を参照してください。

---

<h2 id="issues">イシューとバグ</h2>

JDLは[GitHubで利用可能であり](https://github.com/jhipster/jhipster-core)、JHipsterと同じ
[コントリビューションガイドライン]( https://github.com/jhipster/generator-jhipster/blob/main/CONTRIBUTING.md)に従っています。

ライブラリ自体に関するイシューおよびプルリクエストの送信については、プロジェクトを使用してください。

- [JDLイシュートラッカー](https://github.com/jhipster/jhipster-core/issues)
- [JDLプルリクエスト](https://github.com/jhipster/jhipster-core/pulls)

何かを送信するときは、できるだけ正確である必要があります。
  - **1つの投稿されたイシューには、1つの問題**（または1つの要求/質問）のみが含まれている必要があります。
  - プルリクエストは歓迎されますが、本当に理解できるようにするため、コミットは「アトミック」である必要があります。
