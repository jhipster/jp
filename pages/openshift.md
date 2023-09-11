---
layout: default
title: Openshift
permalink: /openshift/
redirect_from:
  - /openshift.html
sitemap:
    priority: 0.7
    lastmod: 2017-04-30T00:00:00-00:00
---

# [BETA] OpenShiftへのデプロイ

**注意!** これは**BETA**品質の開発中リリースである、新しいサブジェネレータです!フィードバックをお待ちしています!ハッピーOpenShifting!!!

このサブジェネレータを使用すると、JHipsterアプリケーションを[Openshift Container Platform](https://www.openshift.com/) / [OpenShift Origin](https://www.openshift.org/)にデプロイできます。

[![]({{ site.url }}/images/logo/logo-openshift.png)](https://www.openshift.com/)

## 開発中

- MongoとCassandraのレプリケーションモードはまだテストされていません。

## インストールオプション

OpenShiftには2つのオプションがあります。

- OpenShift Origin - OpenShiftを支えるオープンソースのアップストリームプロジェクト
- OpenShift Container Platform - Red Hatがサポートするエンタープライズコンテナアプリケーションプラットフォーム

## Minishift

[Minishift](https://github.com/minishift/minishift)は、オールインワンのOpenShift VMをローカルで実行するのに役立つツールキットです。Minishiftは、ラップトップ上のVM内でシングルノードのOpenShiftクラスタを実行し、ユーザーがローカルで試すことができるようにします。

Minishiftでは、OpenShiftクラスタがプロビジョニングされている仮想マシンを起動するためのハイパーバイザが必要です。Minishiftを起動する前に、選択したハイパーバイザがシステムにインストールされ、有効になっていることを確認してください。

## 前提条件

次をインストールする必要があります。

- [Docker](https://docs.docker.com/installation/#installation)
- Hypervisor - お使いのOSに応じて、さまざまなオプションを選択できます

Dockerレジストリが必要です。レジストリがない場合は、公式の[Docker Hub](https://hub.docker.com/)を使用できます。

Minishiftでは、OriginとContainer Platformの両方をローカルで試すことができます。

- [OpenShift Origin](https://github.com/minishift/minishift)
- [OpenShift Container Platform](https://developers.redhat.com/products/cdk/overview/) - Red Hat Container Development Kitは、Red Hat Enterprise Linuxをベースに構築済みコンテナ開発環境がパッケージ化されたMinishiftを提供します。開発者は、[redhat.com](https://developers.redhat.com)から登録およびダウンロードすることにより、開発目的で無料のRed Hat Enterprise Linux®Developer Suiteサブスクリプションを介してRed Hat Container Development Kitを入手できます。

このサブジェネレータは、OriginとContainer Platformの両方で正常に動作し、同じDockerのイメージバージョンを使用します。

## サブジェネレータの実行

OpenShiftの設定ファイルを生成するには、project/rootフォルダで次のコマンドを実行します。

`jhipster openshift`

次に、アプリケーションをデプロイするためのすべての質問に答えます。


### Which *type* of application would you like to deploy?（どの*種類*のアプリケーションを展開しますか?）

アプリケーションのタイプは、マイクロサービスとモノリスのどちらをデプロイするかによって異なります。


### Enter the root directory where your applications are located（アプリケーションが格納されているルートディレクトリを入力してください）

パスを入力してください。すべてのOpenShiftジェネレータファイルはこのパスに保存されます。


### Which applications do you want to include in your OpenShift configuration?（どのアプリケーションをOpenShift構成に含めますか?）

アプリケーションを選択します。


### Enter the admin password used to secure the JHipster Registry admin（JHipsterレジストリの管理者を保護するために使用する管理者パスワードを入力してください）

<<<<<<< HEAD
この質問は、マイクロサービスアーキテクチャを選択した場合にのみ表示されます。
=======
This question is only displayed if you choose microservices architecture with JHipster Registry.
>>>>>>> upstream/main


### What should we use for the OpenShift namespace?（OpenShiftネームスペースには何を使用しますか?）

これは、すべてのサービスがデプロイされ、生成されたファイルがこのテンプレートにタグ付けされるOpenShiftプロジェクトスペースです。


### Which *type* of database storage would you like to use?（どの*タイプ*のデータベースストレージを使用しますか?）

この質問は、選択したアプリケーションのいずれかでデータベースタイプが選択されている場合にのみ表示されます。これにより、一時的または永続的なストレージオプションが求められます。コンテナは本質的に一時的です（データは再起動/障害の間は保持されません）。永続ストレージオプションを使用すると、
NFS、EBSなどの外部ストレージをマウントできるため、データは再起動と障害の間も存続します。


### What should we use for the base Docker repository name?（ベースのDockerリポジトリ名には何を使用しますか?）

メインレジストリとして[Docker Hub](https://hub.docker.com/)を選択すると、Docker Hubログインになります。


### What command should we use for push Docker image to repository?（Dockerイメージをリポジトリにプッシュするために、どのコマンドを使用しますか?）

Docker Hubにプッシュするデフォルトのコマンドは`docker image push`です。
たとえば、Google Cloudを使用してDockerイメージを公開する場合は、`gcloud docker push`になります。


## 展開したアプリケーションを更新

### 新しい展開の準備

アプリケーションがすでにデプロイされている場合は、新しいDockerイメージを構築することで再デプロイできます。

`./mvnw package -Pprod -DskipTests jib:dockerBuild`

Gradleを使用する場合は次のようにします。

`./gradlew -Pprod bootJar jibDockerBuild -x test`

jibプラグインでビルドされたイメージの実行中に問題が発生した場合（`chmod +x entrypoint.sh が許可されない`など）は、sccを更新する必要があります。以下のように
`oc edit scc restricted`および`runAsUser.Type`ストラテジを`RunAsAny`に更新します。

### Docker Hubへのプッシュ

イメージにローカルでタグを付けます。

`docker image tag application username/application`

イメージをDocker Hubにプッシュします。

`docker image push username/application`

## アプリケーションのデプロイ

アプリケーションをデプロイします。

次のいずれかを実行することで、すべてのアプリケーションをデプロイできます。
  `<directoryPath>/ocp/ocp-apply.sh`

または、

  `oc apply -f <directoryPath>/ocp/registry`
  `oc apply -f <directoryPath>/ocp/app1gw`
とします。その後、選択した名前空間に作成されたテンプレートを選択して、OpenShiftコンソールからアプリケーションをインストールします。

これにより、アプリケーションとそれに関連する依存サービス（データベース、elasticsearchなど）のためのOpenShiftデプロイメントと、pod間通信（サービス内部）のためのOpenShiftサービス、および外部からアプリケーションにアクセスするためのルートが作成されます。

## マイクロサービスアプリケーションに関する情報

### サービスレジストリのデプロイ

OpenShiftは、**Kube-DNS**を使用した独自の内部サービスディスカバリ、ConfigMapを使用した一元化された構成管理、EFKスタックを介した一元化されたロギングを特徴としていますが、JHipsterは構成管理にSpring Cloud、サービスディスカバリにEureka/Consul、ログ管理にJHipster-console(ELK)に依存しているため、OpenShiftデプロイメントも同様にサポートしています。

その結果、マイクロサービスアプリケーションの場合、JHipster OpenShiftサブジェネレータは、**JHipster-Registry**（Eurekaベース）または**Consul**をデプロイするためのマニフェストファイルを生成します。さらに、生成されたマイクロサービスとゲートウェイマニフェストには、自身を中央レジストリサービスに登録するための適切な設定が含まれます。

### JHipsterレジストリまたはConsulの管理

JHipster RegistryとConsulでは、[StatefulSets](https://kubernetes.io/docs/concepts/abstractions/controllers/statefulsets/)設定が提供されています。これらは、ステートフルアプリケーションを処理でき、高可用性のためにサービスレジストリを拡張できる、ある種のデプロイメントアーティファクトです。**StatefulSets**は、OpenShiftではまだプロダクション環境で実用可能な機能ではないことに注意してください。テクノロジープレビュー（ベータ）であり、この機能を使用するには**OpenShiftバージョン3.5以上**が必要です。

### Kubernetesでの一元的な設定

一元化された構成は、**Spring Cloud Config Server**（JHipster-Registryを使用する場合）または**Consul Key/Valueストア**（Consulを使用する場合）のいずれかを使用して設定できます。デフォルトでは、構成サーバーは両方とも、以下の形式のプロパティファイルが含まれているOpenShift [ConfigMap](https://docs.openshift.org/latest/dev_guide/configmaps.html)から設定をロードします。

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: application-config
  namespace: default
data:
  application.yml: |- # すべてのアプリケーションで共有されるグローバルプロパティ
jhipster氏:
      security:
        authentication:
          jwt:
            secret: secret
  gateway-prod.yml: |- # "prod"プロファイルのゲートウェイ・アプリケーション・プロパティー
    foo:
      bar: foobar
```

## トラブルシューティングのヒント

- All-in-one VMを実行している場合は、Dockerイメージをプッシュする前に必ず次のコマンドを実行してください。
`eval $(docker-machine env <machine_name>)`
- 永続ストレージでStatefulSetsまたはServicesを実行する際に問題が発生した場合は、永続ボリュームが適切に初期化されていることを確認してください。
- StatefulSetsの実行中に問題が発生した場合は、永続ボリュームの要求を確認します。PVCの初期化に通常よりも時間がかかる場合は、手動で作成してみてください。
- ジェネレータを実行した後、ocコマンドを適用する前に、選択した名前空間**oc project &lt;namespace&gt;**にいることを確認してください。
- elasticsearch、レジストリ、コンソールなどのサービスのイメージプルは、パブリックレジストリからコンテナレジストリにプルする必要があるため、最初は時間がかかります。このために依存サービスのいずれかが失敗した場合は、それが依存するサービスが起動して実行されているときに、それをデプロイしてみてください。
- いくつかのpodの実行に必要なsccサービスを実行するために必要な特権（管理者が必要な場合があります）を持っていることを確認してください。

## 詳細情報

*   [OpenShift Originドキュメント](https://docs.openshift.org/latest/welcome/index.html)
*   [OpenShift Container Platform](https://access.redhat.com/documentation/en/openshift-container-platform/)
*   [Minishift](https://github.com/minishift/minishift#documentation)
*   [OpenShift CLI](https://docs.openshift.org/latest/cli_reference/get_started_cli.html)
