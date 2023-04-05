---
layout: default
title: TLSおよびHTTP/2の使用
permalink: /tls/
sitemap:
    priority: 0.7
    lastmod: 2018-10-04T00:00:00-00:00
---

# <i class="fa fa-lock"></i> 開発におけるTLSとHTTP/2の使用

## はじめに

このページは、（主にテスト目的の）開発でTLSおよびHTTP/2を使用するためのものです。本番構成の場合は、[プロダクションのドキュメントのセキュリティセクション]({{ site.url }}/production/#security)をお読みください。

TLSは、`https://` のURLを持つ場合に使用されるプロトコルであり、最新のブラウザでHTTP/2を使用するために必要です。

主にパフォーマンス上の理由から、アプリケーションをテストするときにこれらのプロトコルを使用すると便利です。

## Spring BootでのTLSとHTTP/2の使用

JHipsterには、TLSとHTTP/2の両方を設定するための特定の設定があります（[共通アプリケーションプロパティのドキュメント]({{ site.url }}/common-application-properties/)を参照）。さらに簡単にするために、次のように設定します。

- JHipsterは、アプリケーションの生成時に自己署名証明書を生成します。
- 特定の`tls`プロファイルが提供されます（[プロファイルのドキュメント]({{ site.url }}/profiles/)を参照）。

提供された自己署名証明書を使用し、TLSとHTTP/2を有効にしてJHipsterを実行するには、`tls`プロファイルを使用する必要があります。

*   Mavenの場合：`./mvnw -Pdev,tls`
*   Gradleの場合：`./gradlew -Ptls`

アプリは`https://localhost:8080/`で使用可能です。

証明書は自己署名されているため、ブラウザから警告が表示されます。アプリケーションにアクセスするには、証明書を無視する（またはインポートする）必要があります。

## Angular、React、またはVue.jsでのTLSとHTTP/2の使用

（WebpackとBrowserSyncを使用して）フロントエンドを実行するために`npm start`を使用する代わりに、`npm run start-tls`を実行すると、`https://localhost:8080/`で実行されているバックエンドに接続されます。

すべては、TLSとHTTP/2がない場合と同じように動作するはずです。
