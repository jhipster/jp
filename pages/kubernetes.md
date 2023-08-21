---
layout: default
title: Kubernetesへのデプロイ
permalink: /kubernetes/
redirect_from:
  - /kubernetes.html
sitemap:
    priority: 0.7
    lastmod: 2018-06-10T00:00:00-00:00
---

# Kubernetesへのデプロイ

JHipsterアプリケーションおよび関連サービスは、次の方法でデプロイできます。

- 標準kubectl/kustomize/skaffoldサブジェネレータ`jhipster kubernetes|k8s`
- Helmサブジェネレータ`jhipster kubernetes-helm|helm-k8s`
- Knativeサブジェネレータ`jhipster kubernetes-knative|knative`

# `jhipster kubernetes | k8s`

このサブジェネレータは、`kubectl/kustomize/skaffold cli`を介して[Kubernetes](http://kubernetes.io/)にデプロイされるマニフェストを生成します。

[![]({{ site.url }}/images/logo/logo-kubernetes.png)](http://kubernetes.io/)

## 制限事項

- Cassandraはまだサポートされていません。
- Kubernetes v1.9以上が必要です。

## 前提条件

次をインストールする必要があります。

- [Docker](https://docs.docker.com/installation/#installation)
- [kubectl](http://kubernetes.io/docs/user-guide/prereqs/)

Dockerのレジストリが必要です。レジストリがない場合は、公式の[Docker Hub](https://hub.docker.com/)を使用できます。

## Minikube

[Minikube](https://github.com/kubernetes/minikube)は、Kubernetesをローカルで実行するのに役立つツールです。Minikubeは、Kubernetesを試したり日常的にKubernetesを使用して開発したりすることを検討しているユーザーむけに、ラップトップ上のVM内で単一ノードのKubernetesクラスタを実行します。

[Kubernetes](http://kubernetes.io/)にプッシュする前にアプリケーションをテストする目的で使用できます。

## サブジェネレータの実行

Kubernetesの設定ファイルを生成するには、新しいフォルダで次のコマンドを実行します。

`jhipster kubernetes | k8s`

次に、アプリケーションをデプロイするためのすべての質問に答えます。

### Which *type* of application would you like to deploy?（どの*種類*のアプリケーションを展開しますか?）

アプリケーションのタイプは、マイクロサービスアーキテクチャをデプロイするか、従来のアプリケーションをデプロイするかによって異なります。

### Enter the root directory where your applications are located（アプリケーションが格納されているルートディレクトリを入力してください）

パスを入力します。

### Which applications do you want to include in your Kubernetes configuration?（どのアプリケーションをKubernetes構成に含めますか?）

アプリケーションを選択します。

### Do you want to setup monitoring for your applications?（アプリケーションのモニタリングを設定しますか?）

オプションを選択します。

### Enter the admin password used to secure the JHipster Registry admin（JHipsterレジストリの管理者を保護するために使用する管理者パスワードを入力してください）

<<<<<<< HEAD
この質問は、マイクロサービスアーキテクチャを選択した場合にのみ表示されます。
=======
This question is only displayed if you choose microservices architecture with JHipster Registry.
>>>>>>> upstream/main

### What should we use for the Kubernetes namespace?（Kubernetesネームスペースには何を使用しますか?）

namespaceに関する[この](http://kubernetes.io/docs/user-guide/namespaces/)ドキュメントを参照してください。

### What should we use for the base Docker repository name?（ベースのDockerリポジトリ名には何を使用しますか?）

メインレジストリとして[Docker Hub](https://hub.docker.com/)を選択すると、それがDocker Hubログインになります。

[Google Container Registry](https://cloud.google.com/container-registry/)を選択した場合は、`gcr.io/[PROJECT ID]`、または`eu.gcr.io/[PROJECT ID]`、`us.gcr.io/[PROJECT ID]`、`asia.gcr.io/[PROJECT ID]`などの地域レジストリになります。詳細は、[イメージのプッシュとプル](https://cloud.google.com/container-registry/docs/pushing-and-pulling)を参照してください。

[Harbor](https://goharbor.io/),[Quay](https://www.openshift.com/products/quay)などの他のレジストリを選択した場合、ログインは`<registry_server>/<repo>/[PROJECT ID]`のようになります。

### What command should we use for push Docker image to repository?（Dockerイメージをリポジトリにプッシュするために、どのコマンドを使用しますか?）

Docker Hubにプッシュするデフォルトのコマンドは`docker image push`です。

Google Container Registryを使用してDockerイメージを公開する場合は、`gcloud docker push`になります。

### Choose the Kubernetes service type for your edge services?（エッジサービスのKubernetesサービスタイプを選択しますか?）

適切なk8sのルーティングタイプを選択します。

これらは標準のプロンプトです。さらに、IstioやIngressなどのオプションを選択すると、他のプロンプトが表示されます。

## 展開したアプリケーションを更新

### 新しい展開の準備

アプリケーションがすでにデプロイされている場合は、新しいDockerイメージを構築することで再デプロイできます。

`./mvnw package -Pprod -DskipTests jib:dockerBuild`

Gradleを使用する場合は次のようにします。

`./gradlew -Pprod bootJar jibDockerBuild -x test`

### Docker Hubへのプッシュ

イメージにローカルでタグを付けます。

`docker image tag application username/application`

イメージをDocker Hubにプッシュします。

`docker image push username/application`

## モノリス/マイクロサービスアプリケーションのデプロイ

次のコマンドを実行すると、すべてのアプリケーションを展開できます。

```
./kubectl-apply.sh -f (default option)  [or] ./kubectl-apply.sh -k (kustomize option) [or] ./kubectl-apply.sh -s (skaffold run)
```

kustomizeを使用してアプリケーションをデプロイできます。

```
kubectl apply -k ./
```

skaffoldを使用してアプリケーションをデプロイできます。

```
skaffold run [or] skaffold deploy
```

アプリケーションとそれに関連する依存サービス（データベース、elasticsearchなど）をデプロイします。

### カスタム名前空間

配置全体に対してカスタム・ネームスペースを指定できます。カスタム・コマンドを実行するには、次の例のようにターゲット・ネームスペースを指定する必要があります。

`kubectl get pods -n <custom-namespace>`

### 導入環境の拡張

次の方法でアプリケーションを拡張できます。

`kubectl scale deployment <app-name> --replicas <replica-count> `

### ダウンタイムなしの導入

Kubernetesで実行中のアプリケーションを更新するデフォルトの方法として、新しいイメージタグをDockerレジストリにデプロイし、それを使って次のようにしてデプロイします。

`kubectl set image deployment/<app-name>-app <app-name>=<new-image>`

livenessProbesとreadinessProbeを使用すると、サービスの可用性を確保するために、アプリケーションの状態をKubernetesに通知できます。ダウンタイムをゼロにしてデプロイする場合は、各アプリケーションに少なくとも2つのレプリカが必要です。これは、ローリングアップグレード戦略では、新しいレプリカを配置するために、実行中のレプリカを最初に停止するためです。1つのレプリカのみを実行すると、アップグレード中に短いダウンタイムが発生します。

### Kubernetesでのサービスレジストリのデプロイ

Kubernetesは**Kube-DNS**を使用した独自の内部サービスディスカバリを特徴としていますが、JHipsterはサービスディスカバリをSpring Cloudに依存しているため、EurekaやConsulのようなサードパーティのサービスレジストリに依存しています。これには、プラットフォームに依存せず、プロダクション環境とローカル開発マシンで同様に動作するという利点があります。

その結果、マイクロサービスアプリケーションの場合、JHipster Kubernetesサブジェネレータは、**JHipster-Registry**（Eurekaベース）や**Consul**などのサービスレジストリをデプロイするためのKubernetesマニフェストファイルを生成します。さらに、生成されたマイクロサービスとゲートウェイKubernetesマニフェストには、自身を中央レジストリに登録するための適切な設定が含まれます。

### KubernetesでのJHipsterレジストリまたはConsulの管理

JHipster RegistryとConsulの場合、[StatefulSets](https://kubernetes.io/docs/concepts/abstractions/controllers/statefulsets/)設定が提供されます。これらは、ステートフルアプリケーションを処理でき、高可用性のためにサービスレジストリを拡張できる、ある種のKubernetesリソースです。EurekaとConsulの高可用性の詳細については、それぞれのドキュメントを参照してください。

### Kubernetesでの一元的な設定

一元化された設定は、**Spring Cloud Config Server**（JHipster Registryを使用する場合）または**Consul Key/Valueストア**（Consulを使用する場合）を使用して設定できます。デフォルトでは、両方の設定サーバは、次の形式のプロパティファイルを含むKubernetesの[ConfigMap](http://kubernetes.io/docs/user-guide/configmap/)から設定をロードします。

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: application-config
  namespace: default
data:
  application.yml: |- # すべてのアプリケーションで共有されるグローバルプロパティ
    jhipster:
      security:
        authentication:
          jwt:
            secret: secret
  gateway-prod.yml: |- # "prod"プロファイルのゲートウェイ・アプリケーション・プロパティー
    foo:
      bar: foobar
```

デフォルトでは、コンフィギュレーションサーバは開発モードで実行されます。つまり、YAMLプロパティファイルはファイルシステムから直接読み込まれ、変更時にホットリロードされます。本番環境では、[JHipsterレジストリ設定サーバー]({{ site.url }}/jhipster-registry)および[Consul config server]({{ site.url }}/consul)のマイクロサービスドキュメントで説明されているように、Gitリポジトリから設定をセットアップすることをお勧めします。

### ヘッドレスサービスの公開

レジストリはKubernetesのヘッドレスサービスを使用してデプロイされるため、プライマリサービスにはIPアドレスがなく、ノードポートの取得はできません。次を使用して、任意のタイプのセカンダリサービスを作成できます。

`kubectl expose service jhipster-registry --type=NodePort --name=exposed-registry `

詳細を調べるには、次のようにします。

`kubectl get svc exposed-registry `

JHipsterレジストリをスケーリングするには、次のようにします。

`kubectl scale statefulset jhipster-registry --replicas 3 `

## モニタリングツール

サブジェネレータは、アプリケーションで使用するためのモニタリングツールと設定を提供します。

### Prometheusメトリクス

まだインストールされていない場合は、[CoreOSによるPrometheusオペレータ](https://github.com/coreos/prometheus-operator)をインストールします。

`kubectl create -f https://raw.githubusercontent.com/coreos/prometheus-operator/master/bundle.yaml`

**ヒント**:アプリケーションでprometheusメトリクスを有効にして保護する方法の詳細については、[モニタリングのドキュメント]({{ site.url }}/monitoring/#configuring-metrics-forwarding)を参照してください。

アプリケーションのPrometheusインスタンスは、次のコマンドを使用して表示できます。

`kubectl get svc prometheus-appname `

## Kubernetesを活用する

Kubernetesは、マイクロサービスのデプロイを支援するために、次のような多くの機能をすぐに利用できるようしています。
* サービスレジストリ - Kubernetesの`Service`は、サービスレジストリとDNS名を介してのルックアップを提供するファーストクラスの市民です。
* ロードバランシング - Kubernetes ServiceはL4ロードバランサとして機能します。
* ヘルスチェック - liveness probeとreadiness probeは、サービスの状態を判断するのに役立ちます。
* 設定 - Kubernetesの`ConfigMap`は、アプリケーションの外部で設定を保存および適用するために使用できます。

Kubernetesの機能を使用することには、いくつかのメリットがあります。
* シンプルなデプロイ
* Eureka/Consulの追加導入が不要
* Spring Cloud Gatewayによるリクエストのプロキシ/ルーティングが不要
* Spring Cloud Load Balancerが不要

同時に、いくつかの欠点もあります。
* JHipsterレジストリを介したアプリケーション管理はありません - この機能はSpring Cloudの`DiscoveryClient`に依存しています。これは将来更新され、`spring-cloud-kubernetes`が追加される可能性があります。
* ローカルDocker Composeのサポートはありません - ローカル開発には`minikube`を使用し、トラフィックのルーティングにはIngressを使用する必要があります。
* リクエストレベルのロードバランシングなし - Kubernetes Serviceは、接続ごとにロードバランシングを行うL4ロードバランサです。リクエストレベルのロードバランシングにはIstioを使用します（下記参照）。

### Kubernetesをサービスレジストリとして使用する

EurekaやConsulに依存しないようにするには、サービスディスカバリを完全に無効にする必要があります。
* `Which service discovery server do you want to use?（どのサービス検出サーバーを使用しますか?）`というメッセージが表示されたら、`No service discovery（サービス検出なし）`を選択します。

JHipster Gatewayは通常、APIコールをフロントし、Spring Cloud Gatewayを使用してこれらのコールをルーティングします。サービスレジストリがなければ、Spring Cloud Gatewayを介したルーティングは機能しません。トラフィックをマイクロサービスにルーティングするには、Kubernetes Ingressを使用する必要があります。
* `Choose the kubernetes service type for your edge services（エッジサービスのKubernetesサービスタイプを選択してください）`と尋ねられたら、`Ingress`を選択します。

## Istio

マイクロサービスは、[Istio](https://istio.io)対応のKubernetesクラスタにデプロイできます。Kubernetesがマイクロサービスのデプロイと構成を管理するのに対して、Istioは、リクエストレベルのロードバランシング、リトライ、サーキットブレーカ、トラフィックルーティング/スプリットなど、サービス間通信を管理できます。

Istioサポートを有効にするには、次の手順に従います。
* `Do you want to configure Istio?（Istioを設定しますか?）`というメッセージと尋ねられたら、Istioオプションのいずれかを選択します。
* `Do you want to generate Istio route files（Istioルートファイルを生成しますか）`と尋ねられたら、`Yes`を選択して、サーキットブレーカなどのためのデフォルト設定を生成します。

## トラブルシューティング

> 'imagePullBackoff'によりアプリケーションがプルされません

Kubernetesクラスタがアクセスしているレジストリを確認してください。プライベートレジストリを使用している場合は、`kubectl create secret docker-registry`によって名前空間に追加する必要があります（詳細については、[ドキュメント](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)を確認してください）。

> アプリケーションが起動する前に停止しまいます

これは、（Minikubeなど）クラスタのリソースが少ない場合に発生する可能性があります。デプロイのlivenessProbeの`initialDelySeconds`値を増やしてください。

> クラスタに多くのリソースがあるにもかかわらず、アプリケーションの起動が非常に遅くなります

デフォルトの設定は、中規模クラスタ用に最適化されています。JAVA_OPTS環境変数、リソース要求、および制限を自由に増やして、パフォーマンスを向上させることができますが、注意してください!

> Prometheusを選択しましたが、ターゲットが表示されません

これは、Prometheusオペレータの設定とクラスタ内のアクセス制御ポリシーに依存します。RBACの設定を機能させるには、バージョン1.6.0以降が必要です。

> Prometheusを選択しましたが、ターゲットがスクレーピングされません

これは、あなたのアプリケーションがおそらくMaven/Gradleの`prometheus`プロファイルを使って構築されていないことを意味します。

> 複数のレプリカを実行しているときに、Liquibaseの初期化中にSQLベースのマイクロサービスが停止しまう

データベースのchangelogロックが破損することがあります。`kubectl exec -it`を使用してデータベースに接続し、liquibasesの`databasechangeloglock`テーブルのすべての行を削除する必要があります。

# `jhipster kubernetes-helm | k8s-helm`

このサブジェネレータは、`helm cli`を介して[Kubernetes](http://kubernetes.io/)にデプロイされるマニフェストを生成します。

## 前提条件

このサブジェネレータによって生成されたマニフェストを使用するには、`helm cli`をインストールする必要があります。インストール手順については、[このリンク](https://github.com/helm/helm)に従ってください。これには`helm 2.12.x以降`が必要です。

Helmをインストールしたら、次のリポジトリを追加する必要があります。
```
helm repo add stable https://kubernetes-charts.storage.googleapis.com
helm repo add incubator https://kubernetes-charts-incubator.storage.googleapis.com
```
これらのリポジトリは、このサブジェネレータが上記のリポジトリから安定したプロダクショングレードのサービスチャートを取得するため、ローカルキャッシュに追加する必要があります。

このサブジェネレータは、アプリケーションのマニフェストに`kubernetes`サブジェネレータを使用し、アプリケーションで参照されているデータベース、elasticsearch、prometheusなどのサービスイメージを上記のリポジトリから取得します。

## 導入

次のコマンドを実行すると、すべてのアプリケーションをデプロイできます。

```
bash helm-apply.sh (or) ./helm-apply.sh
```

`helm-apply.sh`は常にクリーンインストールを実行します。同じIDを持つ既存のグラフが削除されてから、クリーンインストールが実行されます。

次のコマンドを実行すると、すべてのアプリケーションをアップグレードできます（生成されたマニフェストに変更を加えた場合）。

```
bash helm-upgrade.sh (or) ./helm-upgrade.sh
```

# `jhipster kubernetes-knative | knative`

このサブジェネレータは、では`kubectl or helm cli`を通して[Kubernetes](http://kubernetes.io/)にデプロイされるマニフェストを生成します。選択されたプロンプトの応答に基づいて、いずれかのCLIのマニフェストを生成します。

## 前提条件

このサブジェネレータはIstioに依存しています。このサブジェネレータによって生成されたマニフェストを使用するには、クラスタにistioとkntaiveがインストールされている必要があります。インストール手順については、[このリンク](https://knative.dev/docs/install/)に従ってください。`knative 0.8.x以降`が必要です。

## デプロイ

Kubernetesジェネレータを使用してデプロイすることを選択した場合は、次のコマンドを実行します。
```
bash kubectl-knative-apply.sh (or) ./kubectl-knative-apply.sh
```

Helmジェネレータを使用してデプロイすることを選択した場合は、次のコマンドを実行します。
```
bash helm-knative-apply.sh (or) ./helm-knative-apply.sh
```
`helm-knative-apply.sh`は、常にクリーンインストールを実行します。同じIDを持つ既存のグラフが削除されてから、クリーンインストールが実行されます。

次のbashコマンドを実行すると、すべてのアプリケーションをアップグレードできます（生成されたマニフェストに変更を加えた場合）。

```
bash helm-knative-upgrade.sh (or) ./helm-knative-upgrade.sh
```

## 詳細情報

*   [Kubernetesのドキュメント](http://kubernetes.io/docs/)
