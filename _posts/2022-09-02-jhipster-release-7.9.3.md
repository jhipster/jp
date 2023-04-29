---
layout: default
title: リリース 7.9.3
---

# JHipsterリリース v7.9.3

これは、JHipster v7の新しいパッチリリースで、[313個のクローズされたチケットとマージされたプルリクエスト](https://github.com/jhipster/generator-jhipster/issues?q=milestone%3A7.9.3+is%3Aclosed)があります。

## 最も重要な新機能とアップグレード

- 値のないjdl検索オプションを許可 - [#19485](https://github.com/jhipster/generator-jhipster/pull/19485)
- Keycloak v19のサポート - [#19540](https://github.com/jhipster/generator-jhipster/pull/19540)
- MSSQLに関連するいくつかの修正 - [#19348](https://github.com/jhipster/generator-jhipster/pull/19348) [#19336](https://github.com/jhipster/generator-jhipster/pull/19336) [#19323](https://github.com/jhipster/generator-jhipster/pull/19323)
- Local Blueprintのサポート - [#19451](https://github.com/jhipster/generator-jhipster/pull/19451)
- generate-blueprintワークフローの修正 - [#19594](https://github.com/jhipster/generator-jhipster/pull/19594)
- Spring Boot 2.7.3へのアップグレード - [#19468](https://github.com/jhipster/generator-jhipster/pull/19468)
- 多数のライブラリのアップグレード

## クローズされたチケットとマージされたプルリクエスト

いつものように、**[すべてのクローズされたチケットとマージされたプルリクエストをここで確認できます](https://github.com/jhipster/generator-jhipster/issues?q=milestone%3A7.9.3+is%3Aclosed)**。

## アップグレード方法

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

## ヘルプとバグ

このリリースで問題が発生した場合は、遠慮なく次のことを行ってください。

- [bug tracker](https://github.com/jhipster/generator-jhipster/issues?state=open)にバグを追加します。
- [Stack Overflow](http://stackoverflow.com/tags/jhipster/info)に質問を投稿します。

問題が緊急のバグまたはセキュリティの問題である場合は次のことを行ってください。

- [@jhipster](https://twitter.com/jhipster)のTwitterアカウントに連絡をお願いします。
