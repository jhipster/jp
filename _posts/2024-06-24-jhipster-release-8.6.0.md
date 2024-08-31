---
layout: default
title: リリース 8.6.0
---

# JHipster v8.6.0 リリース

これはJHipster v8のマイナーリリースです。

8.5.0リリース以降、[メインブランチで216のクローズされた課題とプルリクエスト](https://github.com/jhipster/generator-jhipster/issues?q=is:closed+milestone:8.6.0)が含まれています。

## 新機能

* Spring Boot 3.3.1へのアップグレード ([#26490](https://github.com/jhipster/generator-jhipster/pull/26490))
* Angular 18へのアップグレード ([#26213](https://github.com/jhipster/generator-jhipster/pull/26213))
* Java 22のサポート追加 ([#25645](https://github.com/jhipster/generator-jhipster/pull/25645) と [#26495](https://github.com/jhipster/generator-jhipster/pull/26495))
* Maven v3.9.8へのアップグレード ([#26452](https://github.com/jhipster/generator-jhipster/pull/26452))
* Gradle v8.8へのアップグレード ([#26329](https://github.com/jhipster/generator-jhipster/pull/26329))
* Node v20.15.0へのアップグレード ([#26494](https://github.com/jhipster/generator-jhipster/pull/26494))
* Keycloak 25.0.0へのアップグレード ([#26420](https://github.com/jhipster/generator-jhipster/pull/26420))
* Gatlingの修正: 非推奨のプラグイン設定オプションの削除 ([#26493](https://github.com/jhipster/generator-jhipster/pull/26493))
* 不要な`npmw`変数の削除 ([#26436](https://github.com/jhipster/generator-jhipster/pull/26436))
* Docker Composeのバージョンが古い ([#26438](https://github.com/jhipster/generator-jhipster/pull/26438))
* `ci:server:await`スクリプトの常時追加 ([#26393](https://github.com/jhipster/generator-jhipster/pull/26393))
* MySQL 8.4.0がDockerで起動するよう修正 ([#26359](https://github.com/jhipster/generator-jhipster/pull/26359))
* 内部クラスに注釈を追加しないよう修正 ([#26345](https://github.com/jhipster/generator-jhipster/pull/26345))
* MariaDB 11.4.2へのアップグレード ([#26346](https://github.com/jhipster/generator-jhipster/pull/26346))
* Sonar: UserDTOが`equals()`をオーバーライドしているため、`hashCode()`もオーバーライドする必要がある ([#26325](https://github.com/jhipster/generator-jhipster/pull/26325))
* ロガーを'private static final'にするべき ([#26532](https://github.com/jhipster/generator-jhipster/pull/26532))

### :computer: フロントエンド

* [Angular] `tableRow.injector.get`の非推奨シグネチャの修正 ([#26516](https://github.com/jhipster/generator-jhipster/pull/26516) と [#26529](https://github.com/jhipster/generator-jhipster/pull/26529))
* [Angular] Sonar: コンストラクタでのみ割り当てられるフィールドはreadonlyにするべき ([#26514](https://github.com/jhipster/generator-jhipster/pull/26514))
* [Angular] `throwError()`関数の非推奨対応 ([#26515](https://github.com/jhipster/generator-jhipster/pull/26515))
* [Angular] JhipsterをJHipsterにリネーム ([#26512](https://github.com/jhipster/generator-jhipster/pull/26512))
* [Angular] `HttpClientTestingModule`が非推奨 ([#26511](https://github.com/jhipster/generator-jhipster/pull/26511))
* [Angular] Bootswatch Quartzテーマの入力フィールドスタイル修正 ([#26507](https://github.com/jhipster/generator-jhipster/pull/26507))
* [Angular] Sonar: `InfiniteScrollModule`が非推奨 ([#26465](https://github.com/jhipster/generator-jhipster/pull/26465))
* [Angular] Sonar: `HttpClientModule`が非推奨 ([#26464](https://github.com/jhipster/generator-jhipster/pull/26464))
* [Angular] 非推奨のRxJSメソッド（throwError）の修正 ([#26336](https://github.com/jhipster/generator-jhipster/pull/26336))
* [Angular] 非推奨メソッド（angular/core/testing）の修正 ([#26335](https://github.com/jhipster/generator-jhipster/pull/26335))
* [Angular] `signal contentChild`の使用 ([#26334](https://github.com/jhipster/generator-jhipster/pull/26334))
* [React] OAuth2ログインとログアウトの問題修正 ([#26384](https://github.com/jhipster/generator-jhipster/pull/26384))
* ドキュメントでNodeのインストールを要求する代わりに`./npmw`の使用を推奨 ([#26437](https://github.com/jhipster/generator-jhipster/pull/26437))
* 初期テキスト方向設定の修正 ([#26406](https://github.com/jhipster/generator-jhipster/pull/26406))
* エンティティがフィルタリングをサポートしている場合、関連付けをフィルタリングしないよう修正 ([#26357](https://github.com/jhipster/generator-jhipster/pull/26357))
* `.eslintignore`のクリーンアップ ([#26453](https://github.com/jhipster/generator-jhipster/pull/26453))

### :scroll: その他

- いくつかの内部改善とブループリントの最適化

## クローズされたチケットとマージされたプルリクエスト

詳細は[GitHub 8.6.0のリリースノート](https://github.com/jhipster/generator-jhipster/releases/tag/v8.6.0)をご覧ください。

いつも通り、**[クローズされたすべてのチケットとマージされたプルリクエストはこちらから確認できます](https://github.com/jhipster/generator-jhipster/issues?q=is:closed+milestone:8.6.0)**。

## インストール方法

JHipster v8.6.0をインストールするには:

    npm install -g generator-jhipster

JHipster Dockerイメージでも利用可能です。ソースコードから自動的にビルドされます。

- [JHipster Online](https://start.jhipster.tech)
- [JHipster Devbox](https://github.com/jhipster/jhipster-devbox)

## アップグレード方法

**自動アップグレード**

自動アップグレードには、既存のアプリケーションで[JHipster upgradeサブジェネーター]({{ site.url }}/upgrading-an-application/)を使用します。

JHipsterのバージョンをアップグレードします。

```
npm update -g generator-jhipster
```

その後、アップグレードサブジェネレーターを実行します。

```
jhipster upgrade
```

より高度なアップグレード機能には、[migrate blueprint](https://github.com/jhipster/generator-jhipster-migrate)も使用できます。

```
npm i -g generator-jhipster-migrate
jhipster-migrate
```

**手動アップグレード**

手動アップグレードの場合、まずJHipsterのバージョンを以下のようにアップグレードします。

```
npm update -g generator-jhipster
```

既存のプロジェクトがある場合は、生成されたJHipsterバージョンが引き続き使用されます。
プロジェクトをアップグレードするには、まず`node_modules`フォルダを削除してから、以下を実行します。

```
jhipster
```

JHipster 8.0以降、このコマンドはプロジェクトとそのすべてのエンティティを更新します。

エンティティサブジェネレーターを再度実行することで、エンティティを個別に更新することもできます。たとえば、エンティティの名前が _Foo_ の場合は、以下を使用します。

```
jhipster entity Foo
```

## ヘルプとバグ

このリリースで問題が見つかった場合は、ためらわずに以下を行ってください。

- [バグトラッカー](https://github.com/jhipster/generator-jhipster/issues?state=open)にバグを追加する
- [Stack Overflow](http://stackoverflow.com/tags/jhipster/info)に質問を投稿する
- [GitHub](https://github.com/jhipster/generator-jhipster/discussions)で新しいディスカッションを開始する

問題が緊急のバグやセキュリティ問題である場合は、以下を行ってください。

- X (旧Twitter)で[@jhipster](https://twitter.com/jhipster)に連絡する
