---
layout: default
title: リリース 7.9.0
---

JHipsterリリース v7.9.0
==================

これは、JHipster v7の新しいマイナーリリースで、[958個のクローズされたチケットとマージされたプルリクエスト](https://github.com/jhipster/generator-jhipster/issues?q=milestone%3A7.9.0+is%3Aclosed)があります。


最も重要な新機能とアップグレード
-------------

- spring-bootバージョンを2.7.2にアップデート - [#19218](https://github.com/jhipster/generator-jhipster/pull/19218)
- Angularバージョンを14にアップグレード - [#18586](https://github.com/jhipster/generator-jhipster/pull/18586)
- reactのバージョンを18に更新 - [#18823](https://github.com/jhipster/generator-jhipster/pull/18823)
- cypressをバージョン10に移行 - [#18854](https://github.com/jhipster/generator-jhipster/pull/18854)
- generate-blueprintでカスタムジェネレータを生成するサポートを追加（モジュールを置き換え） - [#18306](https://github.com/jhipster/generator-jhipster/pull/18306)
- jdlにマイクロフロントエンドのサポートを追加 - [#18254](https://github.com/jhipster/generator-jhipster/pull/18254)
- マイクロサービスとマイクロフロントエンドの混在のサポートを追加 - [#18632](https://github.com/jhipster/generator-jhipster/pull/18632)
- liquibase xsd changelogの最新バージョンを使用 - [#19029](https://github.com/jhipster/generator-jhipster/pull/19029)
- elasticsearchのページ区切りを修正 - [#18882](https://github.com/jhipster/generator-jhipster/pull/18882)
- ElasticSearchのエンティティインデックス化の新インタフェースを実装 - [#18741](https://github.com/jhipster/generator-jhipster/pull/18741)
- sqlのテストコンテナを使用 - [#18513](https://github.com/jhipster/generator-jhipster/pull/18513)
- keycloakバージョンを18.0.0にアップグレード - [#18441](https://github.com/jhipster/generator-jhipster/pull/18441)
- 多数のライブラリのアップグレード

クローズされたチケットとマージされたプルリクエスト
------------
いつものように、__[すべてのクローズされたチケットとマージされたプルリクエストをここで確認できます](https://github.com/jhipster/generator-jhipster/issues?q=milestone%3A7.9.0+is%3Aclosed)__。

アップグレード方法
------------

**自動アップグレード**

自動アップグレードの場合は、既存のアプリケーションで[JHipsterアップグレードサブジェネレータ]({{ site.url }}/upgrading-an-application/)を使用します。

JHipsterのバージョンをアップグレードします。

```
npm update -g generator-jhipster
```

次に、アップグレードサブジェネレータを実行します。

```
jhipster upgrade
```

**手動アップグレード**

手動アップグレードの場合は、まず次のコマンドを使用してJHipsterのバージョンをアップグレードします。

```
npm update -g generator-jhipster
```

既存のプロジェクトがある場合は、そのプロジェクトは生成されたJHipsterのバージョンをそのまま使用します。
プロジェクトをアップグレードするには、まず`node_modules`フォルダを削除してから、次のコマンドを実行する必要があります。

```
jhipster
```

次のコマンドを実行して、プロジェクトとすべてのエンティティの更新もできます。

```
jhipster --with-entities
```

また、エンティティサブジェネレータを再度実行し、エンティティの1つずつの更新もできます。たとえば、エンティティの名前が _Foo_ の場合は以下となります。

```
jhipster entity Foo
```


ヘルプとバグ
--------------

このリリースで問題が発生した場合は、遠慮なく次のことを行ってください。

- [bug tracker](https://github.com/jhipster/generator-jhipster/issues?state=open)にバグを追加します。
- [Stack Overflow](http://stackoverflow.com/tags/jhipster/info)に質問を投稿します。

問題が緊急のバグまたはセキュリティの問題である場合は次のことを行ってください。

- [@jhipster](https://twitter.com/jhipster)のTwitterアカウントに連絡をお願いします。
