---
layout: default
title: Google Cloud Platformへのデプロイ
permalink: /gcp/
sitemap:
    priority: 0.5
    lastmod: 2018-10-02T00:00:00-00:00
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

## Google App Engineにデプロイ

Google App Engineは、完全に管理されたPlatform as a Serviceであり、負荷がかかっているアプリケーションインスタンスを自動的にスケールアップし、使用されていない場合はゼロにスケールダウンできます。

Google App Engineジェネレータを使用して、JHipsterアプリケーションを生成およびデプロイできます。Google App Engineジェネレータは、Cloud SQL MySQL/PostgreSQLデータベースを使用して、モノリスとマイクロサービスアプリケーションをサポートします。

#### Google App Engineへのモノリスのデプロイ

1. 新しいモノリスアプリケーションを生成します。：`jhipster`
1. Google App Engineジェネレータを実行します。：`jhipster gae`
1. まったく新しいアプリケーションを作成する場合は、オプションで新しいCloud SQLインスタンスを作成します。

このジェネレータは次のことを行います。
1. App Engineインスタンスとスケーリング構成を記述する`src/main/appengine/app.yaml`を追加します。
1. Maven/GradleにApp Engineプラグインを追加します。

デプロイするにあたり、
現在、Google App Engineジェネレータは、[App Engine Standard (Java 11)](https://cloud.google.com/appengine/docs/standard/java11/)環境へのデプロイのみをサポートしていることに注意してください。

- App Engineプラグインを使用してデプロイします。：`./mvnw package appengine:deploy -DskipTests -Pgae,prod,prod-gae`またはGradleでは`./gradlew appengineDeploy -Pgae -Pprod-gae`を使用します。

#### Google App Engineへのマイクロサービスのデプロイ

[Google CloudはGAE上のマイクロサービスアーキテクチャをサポート](https://cloud.google.com/appengine/docs/standard/java/microservices-on-app-engine)しており、
各マイクロサービスを独立したサービスとして分離させています。[`dispatch.yaml`ファイル](https://cloud.google.com/appengine/docs/standard/java11/reference/dispatch-yaml)を使用して、
リクエストをゲートウェイから各マイクロサービスにルーティングします。そのため、マイクロサービスをGAEにデプロイするには、
ゲートウェイと各マイクロサービスを別々のサービスとしてデプロイする必要があります。

実行する必要がある手順は次のとおりです。

1. 各マイクロサービスでGAEサブジェネレータを実行します。ゲートウェイアプリケーションのセットアップはこれに依存するため、これを最初のステップとして実行することが
重要です。

2. ゲートウェイアプリケーションでGAEサブジェネレータを実行します。これにより、
`dispatch.yaml`ファイルを作成するための追加の質問が表示されます。

3. Mavenの場合は`./mvnw package appengine:deploy -DskipTests -Pgae,prod,prod-gae` を使用して、各マイクロサービスとゲートウェイアプリケーションをデプロイします。
Gradleの場合は`./gradlew appengineDeploy -Pgae -Pprod-gae`です。

**注1:** Windowsを使用している場合は、[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)を使用することをお勧めします。
または[https://github.com/jhipster/generator-jhipster/issues/11249 
](https://github.com/jhipster/generator-jhipster/issues/11249)のようなWindows固有の問題を回避するため、[jhipster-devbox](https://github.com/jhipster/jhipster-devbox)を使用してください。

**注2:** Cloud SQLを使用している場合は、App EngineサービスアカウントにCloud SQLクライアントロールを追加する必要があります。[https://cloud.google.com/sql/docs/mysql/connect-app-engine#setting_up](https://cloud.google.com/sql/docs/mysql/connect-app-engine#setting_up)を参照してください。

さらに、Google App Engineには、アプリケーションを管理するための一連の機能が用意されています。
- トラフィック分割 - アプリケーションの複数のバージョンをデプロイし、トラフィックを異なるバージョンに分割します。これは、カナリアの新しい変更にも最適です。
- Stackdriver Logging - 検索、監視、およびエクスポートが可能な集中型ロギングで、アプリケーションログを自動的にキャプチャおよび保存します。
- エラーレポート - ログのエラーと例外を自動的に抽出し、新しいエラーを通知します。
- クラウドデバッガ - 作業を停止することなく、プロダクションアプリケーションをデバッグできます。問題を診断するためにさらにログメッセージが必要な場合は、アプリケーションを再デプロイ/再起動することなく、新しいログメッセージを追加します。

[Ray Tsang](https://twitter.com/saturnism)と[Ludovic Champenois](https://twitter.com/ludoch)による[Google App Engineジェネレータでの2018 JHipster Confビデオ](https://www.youtube.com/watch?v=J9_MW3HOj5w)では、機能のウォークスルーを見ることができます。
   
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
