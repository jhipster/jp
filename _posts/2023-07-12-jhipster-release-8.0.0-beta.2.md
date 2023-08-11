---
layout: default
title: リリース 8.0.0-beta.2
---

JHipsterリリース v8.0.0-beta.2
==================

これは、JHipster v8の2番目のベータリリースです。

これには、[336以上のクローズされたチケットとメインプロジェクトのプルリクエスト]が含まれています。(https://github.com/jhipster/generator-jhipster/issues?q=is:closed+milestone:8.0.0-beta.2).

_これはベータ版のリリースであるため、通常の方法では入手できません。詳細については、以下を参照してください!_


何が新しくなりましたか?
------------

### :gem: 機能と拡張機能
- Herokuサブジェネレータの改良 [#21892](https://github.com/jhipster/generator-jhipster/pull/21892)
- アプリケーションがゲートウェイまたはモノリスの場合にCORSを有効にする [#22780](https://github.com/jhipster/generator-jhipster/pull/22780)
- jhipster開発用にdevcontainerを追加 [#22814](https://github.com/jhipster/generator-jhipster/pull/22814)

### :computer: Frontend
- 改ページの未翻訳の修正 [#22583](https://github.com/jhipster/generator-jhipster/pull/22583)
- Google Analyticsタグ(analytics.js)をGoogleタグに変更 (gtag.js)  [#22697](https://github.com/jhipster/generator-jhipster/pull/22697)

### :paw_prints: JDL/Internals/Blueprints
- Bump@faker-js/fakerをv8にアップグレード [#22118](https://github.com/jhipster/generator-jhipster/pull/22118)
- Gradle Liquibaseの実行不具合を修正 [#22667](https://github.com/jhipster/generator-jhipster/pull/22667)
- Maven Liquibaseの実行不具合を修正[#22737](https://github.com/jhipster/generator-jhipster/pull/22737)

### :scroll: その他
- 多くの改善
- 多くのライブラリのアップグレード
- 多くのバグ修正


クローズされたチケットとマージされたプルリクエスト
------------
いつものように、__[すべてのクローズされたチケットとマージされたプルリクエストをここで確認できます](https://github.com/jhipster/generator-jhipster/issues?q=is:closed+milestone:8.0.0-beta.2)__。


インストール方法
------------

これはベータ版リリースなので、通常の「安定版」リリースの方法では入手できません。

NPMを使用してJHipster v8.0.0-beta.1をインストールするには、以下のようにします。

    npm install -g generator-jhipster@beta

また、JHipster Dockerイメージも利用可能です。ソースコードから自動的に構築されます。

しかし、これはベータリリースであるため、次のような方法では入手できません。

- [JHipster Online](https://start.jhipster.tech)
- [JHipster Devbox](https://github.com/jhipster/jhipster-devbox)

また、ベータリリースはNPMの特定のベータチャネルを通じても見ることができないことから、`jhipster upgrade`サブジェネレータを使用することもできません。


ヘルプとバグ
--------------

このリリースで問題が発生した場合は、遠慮なく次のことを行ってください。

- [bug tracker](https://github.com/jhipster/generator-jhipster/issues?state=open)にバグを追加します。
- [Stack Overflow](http://stackoverflow.com/tags/jhipster/info)に質問を投稿します。

問題が緊急のバグまたはセキュリティの問題である場合は次のことを行ってください。

- [@jhipster](https://twitter.com/jhipster)のTwitterアカウントに連絡をお願いします。
