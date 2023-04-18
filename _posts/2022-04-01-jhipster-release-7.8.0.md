---
layout: default
title: リリース 7.8.0
---

JHipsterリリース v7.8.0
==================

これはJHipster v7の新しいマイナーリリースで、[263個のクローズされたチケットとマージされたプルリクエスト](https://github.com/jhipster/generator-jhipster/issues?q=milestone%3A7.8.0+is%3Aclosed)があります。


最も重要な新機能とアップグレード
--------------

- Spring Boot v2.6.6へのアップグレード - [#18252](https://github.com/jhipster/generator-jhipster/pull/18252)
- Java 18のサポートを追加 - [#18190](https://github.com/jhipster/generator-jhipster/pull/18190)
- Reactマイクロフロントエンドサポートの実装 - [#18103](https://github.com/jhipster/generator-jhipster/pull/18103)
- Couchbase：リレーションを持つエンティティのページ区切り要求を修正 - [#18007](https://github.com/jhipster/generator-jhipster/pull/18007)
- 多数のライブラリのアップグレード

クローズされたチケットとマージされたプルリクエスト
------------
いつものように、__[すべてのクローズされたチケットとマージされたプルリクエストをここで確認できます](https://github.com/jhipster/generator-jhipster/issues?q=milestone%3A7.8.0+is%3Aclosed)__。

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
