---
layout: default
title:
permalink: /managing-server-errors/
sitemap:
    priority: 0.7
    lastmod: 2018-03-07T00:00:00-00:00
---

# <i class="fa fa-fire-extinguisher"></i> サーバー・エラーの管理

JHipsterはエラー処理のための第一級のサポートを提供しており、エラーページとカスタムメカニズムを提供して、サーバ側でビジネスエラーとテクニカルエラーの両方を処理します。

## エラーページ

JHipsterはSingle-Page Application(SPA)を生成しますが、アプリケーションにアクセスしない（またはアクセスできない）ユーザーのためにカスタム・エラー・ページが必要です。

### 動的エラーページ

JHipsterは一般的なエラーページを提供します。これは[Thymeleaf](https://www.thymeleaf.org/)テンプレートで、`src/main/resources/templates/error.html`にあります。

このページには、サーバー側のエラー・メッセージが表示されます。たとえば、ユーザーが存在しないページにアクセスしようとすると、404エラーが表示され、ページが見つからなかったことがユーザーに通知されます。

### 静的404エラーページ

JHipsterは、`src/main/webapp/404.html`にある特定の静的な404エラーページを提供します。デフォルトでは、このページはJHipsterによって使用されません。JHipster（Apache/NGinx/など）の前にプロキシを使用するプロジェクトのためにここにあるので、JHipsterアプリケーションが使用できない場合でも、プロキシは404エラーページを表示できます。

これはフロントエンドプロキシで特別に設定する必要があります。

## APIエラー

Spring MVC RESTエラーを処理するために、JHipsterは[Zalandoの Problem Spring Webライブラリ](https://github.com/zalando/problem-spring-web)を使用して、豊富なJSONベースのエラーメッセージを提供します。

エンドユーザを支援するために、このライブラリは既知の問題ごとに、詳細を提供する特定のエラーページへのリンクを提供します。これらのリンクは`ErrorConstants`クラスで設定され、既定ではこのWebサイトをポイントします。アプリケーションでは、これらのリンクをカスタマイズし、独自のAPIドキュメントをポイントする必要があります。

利用可能なエラーリンクは次のとおりです。

- [メッセージの問題]({{ site.url }}/problem/problem-with-message)
- [制約違反]({{ site.url }}/problem/constraint-violation)
- [パラメータ化されたメッセージの問題]({{ site.url }}/problem/parameterized)
- [エンティティが見つかりません]({{ site.url }}/problem/entity-not-found)
- [無効なパスワード]({{ site.url }}/problem/invalid-password)
- [Eメールは既に使用されています]({{ site.url }}/problem/email-already-used)
- [ログインは既に使用されています]({{ site.url }}/problem/login-already-used)
- [Eメールが見つかりません]({{ site.url }}/problem/email-not-found)
