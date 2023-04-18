---
layout: default
title: リリース 7.1.0
---

JHipsterリリース v7.1.0
==================

これは、JHipster v7の新しいマイナーリリースで、[947個のクローズされたチケットとマージされたプルリクエスト](https://github.com/jhipster/generator-jhipster/issues?q=milestone%3A7.1.0+is%3Aclosed)があります。

重大な変更
-------------

- React: Reduxツールキットの移行 - [#15033](https://github.com/jhipster/generator-jhipster/issues/15033)
- React: availity-reactstrap-validationからreact-hook-formへの移行 - [#15191](https://github.com/jhipster/generator-jhipster/pull/15191)

最も重要な新機能とアップグレード
-------------

- Angular 12 - [#14980](https://github.com/jhipster/generator-jhipster/pull/14980)
- Angularにマイクロフロントエンドのサポートを追加 - [#15286](https://github.com/jhipster/generator-jhipster/pull/15286)
- AWS Containers Subgeneratorの削除 - [#14637](https://github.com/jhipster/generator-jhipster/pull/14637)
- spring-bootバージョンを2.4.7およびその他の依存関係に更新 - [#15283](https://github.com/jhipster/generator-jhipster/pull/15283)
- フロントエンドアプリケーションファイルのキャッシュ - [#15126](https://github.com/jhipster/generator-jhipster/issues/15126)
- Cypress 7.4.0 - [#14983](https://github.com/jhipster/generator-jhipster/pull/14983)
- JWTRelayがauthorization header無しを許可 - [#14854](https://github.com/jhipster/generator-jhipster/pull/14854)
- デフォルトでBase 64エンコードJWTシークレットを使用 - [#14952](https://github.com/jhipster/generator-jhipster/issues/14952)
- 多数のライブラリのアップグレード

クローズされたチケットとマージされたプルリクエスト
------------
いつものように、__[すべてのクローズされたチケットとマージされたプルリクエストをここで確認できます](https://github.com/jhipster/generator-jhipster/issues?q=milestone%3A7.1.0+is%3Aclosed)__。

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

**ヒント**

[prettier-java](https://github.com/jhipster/prettier-java)を使用してすべてのJavaクラスがすでにフォーマットされているプロジェクトを生成するには、次のコマンドを使用します。

```
jhipster --prettier-java
```

ヘルプとバグ
--------------

このリリースで問題が発生した場合は、遠慮なく次のことを行ってください。

- [bug tracker](https://github.com/jhipster/generator-jhipster/issues?state=open)にバグを追加します。
- [Stack Overflow](http://stackoverflow.com/tags/jhipster/info)に質問を投稿します。

問題が緊急のバグまたはセキュリティの問題である場合は次のことを行ってください。

- [@jhipster](https://twitter.com/jhipster)のTwitterアカウントに連絡をお願いします。
