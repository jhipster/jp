---
layout: default
title: Google Cloud Platformへのデプロイ
permalink: /gcp/
sitemap:
    priority: 0.5
    lastmod: 2023-12-19T00:00:00-00:00
---

# <i class="fa fa-cloud-upload"></i> Google Cloud Platformへのデプロイ

[![Google Cloud Platform]({{ site.url }}/images/logo/logo-gcp.png)](https://cloud.google.com)

JHipsterアプリケーションをGoogle Cloud Platformにデプロイして、次の環境で実行できます。
- [Google Compute Engine](https://cloud.google.com/compute/)を搭載した仮想マシン
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/)を使用したKubernetesのコンテナ
- [Google App Engine](https://cloud.google.com/appengine/)を使ったPlatform as a Service

アプリケーションをデプロイするには、[Google Cloud Platform無料試用版](https://cloud.google.com/free)を入手できます。無料試用中および無料試用の終了後に、[Always Free](https://cloud.google.com/free/)ティアで指定された使用制限までの無料使用を確認してください。

## 始める前に

`gcloud`にCLIでアクセスするには、ローカル環境にgcloud SDKをインストールして認証します。詳細については、次のリンクを参照してください。

- [gcloud SDKのインストール](https://cloud.google.com/sdk/install)

## Google Kubernetes Engineへのデプロイ

Google Kubernetes Engineは、完全に管理されたKubernetesクラスタ・アズ・ア・サービスです。プロビジョニングされたコンテナとJHipsterアプリケーションを、標準のKubernetesコマンドを使用してデプロイできます。

1. APIの有効化：`gcloud services enable container.googleapis.com containerregistry.googleapis.com`
1. `kubectl`CLIがまだインストールされていない場合はインストールします：`gcloud components install kubectl`
1. 新しいGoogle Kubernetes Engineクラスタを作成します：`gcloud container clusters create mycluster --zone us-central1-a --machine-type n1-standard-4`

_その他のオプションについては、GCPの[ゾーン](https://cloud.google.com/compute/docs/regions-zones/)および[マシンタイプ](https://cloud.google.com/compute/docs/machine-types/)を参照してください。_

クラスタが作成されると、JHipster Kubernetesジェネレータを使用してデプロイメント記述子を生成できます。

1. Kubernetesデプロイメントファイルの生成：`jhipster kubernetes`
1. Google Container Registryを使用してプライベート・レジストリにコンテナ・イメージを公開する場合：
  1. **What should we use for the base Docker repository name**（**ベースのDockerリポジトリ名には何を使用すべきか**）には、`gcr.io/YOUR_PROJECT_ID`を設定します。

コンテナイメージを構築します。

1. Google Container Registryを使用する場合は、ローカルのDockerデーモンなしでレジストリに直接ビルドできます：`./mvnw package -Pprod jib:build`
1. それ以外の場合は、Dockerデーモンにビルドします：`./mvnw package -Pprod jib:dockerBuild`

Kubernetesクラスタへデプロイします。

1. Kubernetes設定を適用します：`./kubectl-apply.sh`

Kubernetesジェネレータの全機能については、[Kubernetesへのデプロイ](/kubernetes)を参照してください。

## HTTPSを有効にする

クラスタでHTTPSを有効にするには、Ray Tsang氏の[外部のロードバランシングのドキュメント](https://spring-gcp.saturnism.me/deployment/kubernetes/load-balancing/external-load-balancing)を参照してください。

HTTPSの使用を強制するには、次の設定を`SecurityConfiguration.java`に追加します。

```java
// Spring MVC
http.requiresChannel(channel -> channel
    .requestMatchers(r -> r.getHeader("X-Forwarded-Proto") != null).requiresSecure());

// WebFlux
http.redirectToHttps(redirect -> redirect
    .httpsRedirectWhen(e -> e.getRequest().getHeaders().containsKey("X-Forwarded-Proto")));
```

詳細については、Spring Securityの[Servlet](https://docs.spring.io/spring-security/site/docs/5.5.x/reference/html5/#servlet-http-redirect)および[WebFlux](https://docs.spring.io/spring-security/site/docs/5.5.x/reference/html5/#webflux-http-redirect)のドキュメントを参照してください。
