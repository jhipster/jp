---
layout: default
title: KubernetesとGoogle Cloud SQL
sitemap:
priority: 0.5
lastmod: 2016-11-13T19:00:00-00:00
---

# KubernetesとGoogle Cloud SQL

__このTipは[@bourdux](https://github.com/bourdux)により提出されました__

Kubernetesサブジェネレータを使用してJHipsterアプリケーションを[Google Container Engine](https://cloud.google.com/container-engine/)
にデプロイすることはすでに簡単ですが、デフォルトの動作はデータベース用のGoogle Compute 
Engine VMを作成します。

さらに一歩進んで、フルマネージドのMySQLインスタンスを使用したい場合は、[Google Cloud SQL](https://cloud.google.com/sql/)があります。
自動化されたバックアップ、メンテナンス、レプリケーションにより、高可用性と優れた拡張性を実現します。

このヒント/チュートリアルでは、Google Cloud SQLデータベースをMySQLバックエンドとして使用するJHipsterアプリケーションをGoogle 
Cloudにデプロイする方法を示します。プロセスを簡素化するために、モノリシックアプリケーションを使用します。また、
私のお気に入りのビルドであるMavenビルドも使用します。 :p

## 前提条件

このチュートリアルでは、次のものが必要です。

* Google Cloud Platformアカウント。300ドル相当の無料クレジットで[60日間無料トライアル](https://cloud.google.com/free-トライアル/)を利用できます。
* [Google Cloud SDK](https://cloud.google.com/sdk/)。ほとんどの操作をターミナルから実行します。[対話型インストーラ](https://cloud.google.com/sdk/downloads#interactive)は非常に便利です。
* [Docker](https://www.docker.com/products/overview)
* プロダクションデータベースとしてMySQLを使用するJHipsterアプリケーション

## gcloudとkubectlを初期化する

まず、`gcloud`を使ったことがない場合は、次のコマンドで初期化する必要があります。

    gcloud init

`gcloud`を使用すると、Google Cloud Webコンソールから実行できるほとんどの操作を、
ターミナルから快適に実行できます。まず、`kubectl`をインストールしましょう。

    gcloud components install kubectl

`kubectl`は、Kubernetesクラスタに対してコマンドを実行するためのコマンドラインインタフェースです。
[KubernetesのWebサイト](http://kubernetes.io/docs/user-guide/prereqs/)から直接インストールもできますが、全体的に見て、gcloudのインストールの方が
便利だと思いました。

次に、Google Cloudプロジェクトを作成する必要があります。この目的のためには、Webコンソールを使用する必要があります。gcloudではCLIからプロジェクトを
作成できないためです（アルファ版のためまだありません）。または、[Resource
Manager API](https://cloud.google.com/resource-manager/docs/creating-project)を使用できます。

* [Google Cloud Platform Console](https://console.cloud.google.com)に行き
* **Create Project**をクリックします。
* プロジェクト名を選択し、**Create**をクリックしてプロジェクトIDをメモし、必要に応じてカスタマイズします。

このチュートリアルのために、`jhipster-kubernetes-cloud-sql`という名前を選択しました。

次に、以下の操作が必要です。

* プロジェクトの[billing](https://console.cloud.google.com/billing)を有効にします。
* プロジェクトの[Container Engine API](https://console.cloud.google.com/projectselector/kubernetes/list)を有効にします。
* Compute Engine、Cloud SQL、Container Engineの[API Manager](https://console.cloud.google.com/apis/dashboard)を有効にします。
* [Google Cloud SQL API](https://console.developers.google.com/apis/api/sqladmin/overview)を有効にします。

最後に、現在作業しているプロジェクトを`gcloud`に指示する必要があります。

    gcloud config set project jhipster-kubernetes-cloud-sql

また、デフォルトでインスタンスを作成する場所も指定できます。私は`europe-west1-b`を選びました。
ケチなヨーロッパ人なので :)

    gcloud config set compute/zone europe-west1-b

## Cloud SQLインスタンスの作成

次に、Google Cloud SQLインスタンスを作成する必要があります。これはWebコンソールから行うことができ、利用可能なオプションをよく
理解するのに役立ちます。また、繰り返しますが、`gcloud`の使用もできます。

    gcloud beta sql instances create jhipster-sqlcloud-db --region=europe-west1 --tier=db-f1-micro\
     --authorized-networks=`curl -s ifconfig.co` --backup-start-time=01:00 --enable-bin-log \
     --activation-policy=ALWAYS --storage-type=HDD --storage-size=10GB


このコマンドを使用して、`europe-west1`リージョンに`jhipster-sql-cloud-db`という名前のSQL Cloudインスタンスを作成します。
使用可能な最小のマシンタイプを選択します。使用可能な階層の完全なリストを表示するには、`gcloud sql tiers list`を使用できます。
次に、`mysql`CLIを使用してアクセス用の独自のIPをホワイトリストにし、午前1時UTCから始まるバックアップ時間ウィンドウを設定し、バイナリロギングを有効にして、
アプリケーションに問題が発生した場合に時間を遡ることができるようにします。最後に、マシンを常にアクティブにするように設定し
（第2世代のマシンは使用ごとに課金されるため必要）、HDDストレージ（SSDの方がパフォーマンスは高いが
高価）を設定し、ストレージサイズを最小サイズに設定します。注意：第2世代のSQLインスタンスを作成するには、
ベータ版のgcloudクライアントを使用する必要があります。

インスタンスが開始されたことを確認するには、次のコマンドを使用します。

    gcloud sql instances list
    NAME                   REGION        TIER         ADDRESS         STATUS
    jhipster-sqlcloud-db  europe-west1  db-f1-micro  146.148.21.155  RUNNABLE

IPアドレスをホワイトリストに登録したので、`mysql`を使用してDBインスタンスにアクセスできるはずです。

    mysql --host=146.148.21.155 --user=root --password
    ...
    mysql>

データベースに接続しているので、アプリケーションのデータベースとユーザーを作成します。
[Cloud SQLプロキシ](https://cloud.google.com/sql/docs/sql-proxy)を使用してアプリケーションコンテナからSQLインスタンスに接続するため、
プロキシ経由の接続のみを許可する場合は、ユーザーのホスト名を`cloudsqlproxy~%`に設定します。
このチュートリアルのアプリケーション名は`jhipsterGoogleCloudSql`なので、JHipsterによって生成された構成を使用する場合は、
データベース名も同じ名前にする必要があります。

    mysql> CREATE DATABASE jhipstergooglecloudsql;
    Query OK, 1 row affected (0,03 sec)

    mysql> CREATE USER 'jhipster'@'cloudsqlproxy~%';
    Query OK, 0 rows affected (0,01 sec)

    mysql> GRANT ALL PRIVILEGES ON jhipstergooglecloudsql.* TO 'jhipster'@'cloudsqlproxy~%';
    Query OK, 0 rows affected (0,01 sec)

    mysql> FLUSH PRIVILEGES;
    Query OK, 0 rows affected (0,02 sec)

`application-prod.yml`でデータベースユーザーをjhipsterに変更するのを忘れないでください。

## コンテナクラスタを作成する

[GKE](https://cloud.google.com/container-engine/docs/)を使ってコンテナクラスタを作成しましょう。

    gcloud container clusters create jhipster-sqlcloud-cluster --zone=europe-west1-b --machine-type=g1-small --num-nodes=1

このチュートリアルでは、1つの小さなノードのみを使用します。本番環境では、少なくとも3つのノードが必要です。:)

次に、kubectlにこのクラスタの適切な資格情報を取得させます。

    gcloud container clusters get-credentials jhipster-sqlcloud-cluster

    Fetching cluster endpoint and auth data.
    kubeconfig entry generated for jhipster-sqlcloud-cluster.

## Dockerイメージのビルドとプッシュ

まず、[Kubernetesサブジェネレータ]({{ site.url }}/kubernetes)を実行します。質問には通常どおり回答しますが、
DockerイメージをGoogle Cloudにプッシュしてコンテナエンジンを使用しましょう。"What should we use for the base Docker 
repository name?"（ベースのDockerリポジトリ名には何を使用すべきですか？）という質問には、`gcr.io/jhipster-kubernetes-cloud-sql`で回答します。自身のプロジェクトIDで置き換えてください。dockerイメージプッシュコマンドでは、
プロジェクトコンテナリポジトリにプッシュするために`gcloud docker -- push`を使用します。

イメージを構築します。

    mvn package -Pprod jibDockerBuild

イメージにタグを付けます（自身のjhipsterアプリケーション名で置き換えてください）。v1をタグとして使用することで、アプリケーションの新しいバージョンを
簡単にデプロイしたり、何かがひどくおかしくなった場合にロールバックしたりできます。

    docker image tag jhipstergooglecloudsql gcr.io/jhipster-kubernetes-cloud-sql/jhipstergooglecloudsql:v1

次に、次のようにしてイメージをGoogle Containerエンジンにプッシュできます。

    gcloud docker -- push gcr.io/jhipster-kubernetes-cloud-sql/jhipstergooglecloudsql:v1

## 資格情報を取得してKubernetesに登録する

Cloud SQLプロキシを使用するには、アプリケーションの認証情報を作成し、それらを
Kubernetesに登録する必要があります。完全なプロセスは[Cloud SQLコンテナエンジン接続ドキュメント](https://cloud.google.com/sql/docs/container-engine-connect)で入手できますが、
ここではコマンドを要約します。

JHipsterアプリケーションのサービスアカウントを作成します。

    gcloud iam service-accounts create jhipster-application --display-name="JHipster application"

iamアカウントの完全な名前（キーの生成に使用された電子メール）を取得します。

    gcloud iam service-accounts list
    NAME                                    EMAIL
    JHipster application                    jhipster-application@jhipster-kubernetes-cloud-sql.iam.gserviceaccount.com

サービスアカウントにプロジェクトのエディター権限を付与します。

    gcloud projects add-iam-policy-binding jhipster-kubernetes-cloud-sql \
     --member serviceAccount:jhipster-application@jhipster-kubernetes-cloud-sql.iam.gserviceaccount.com \
     --role roles/editor

キーを作成し、それを`jhipster-credentials.json`に格納します。

    gcloud iam service-accounts keys create \
    --iam-account jhipster-application@jhipster-kubernetes-cloud-sql.iam.gserviceaccount.com jhipster-credentials.json

このキーは後ほど使います。

`kubectl`で鍵を登録します。

    kubectl create secret generic cloudsql-oauth-credentials --from-file=credentials.json=jhipster-credentials.json

## Kubernetesデプロイメント設定を変更する

まず最初に、Cloud SQLインスタンスを使用するため、生成されたmysqlデプロイメントファイルを削除します。

次に、`jhipstergooglecloudsql-deployment.yml`をいくつか変更する必要があります。Cloud SQLプロキシを使用するので、
最初にSpringデータソースのURLをlocalhostに変更する必要があります。

    jdbc:mysql://localhost:3306/jhipstergooglecloudsql?useUnicode=true&characterEncoding=utf8&useSSL=false

次に、バージョン番号をコンテナイメージに追加します。

    image: gcr.io/jhipster-kubernetes-cloud-sql/jhipstergooglecloudsql:v1

次に、サイドカーパターンでクラウドSQLプロキシをデプロイするためのエントリを追加する必要があります。

    - image: b.gcr.io/cloudsql-docker/gce-proxy:1.05
      name: cloudsql-proxy
      command: ["/cloud_sql_proxy", "--dir=/cloudsql",
                "-instances=jhipster-kubernetes-cloud-sql:europe-west1:jhipster-sqlcloud-db=tcp:3306",
                "-credential_file=/secrets/cloudsql/credentials.json"]
      volumeMounts:
        - name: cloudsql-oauth-credentials
          mountPath: /secrets/cloudsql
          readOnly: true
        - name: ssl-certs
          mountPath: /etc/ssl/certs

すでに指摘したように、Cloud SQLインスタンスに接続できるように、
Google APIと通信するためのSSL証明書も提供する必要があります。

最後に、適切なボリュームを追加します。

    volumes:
      - name: cloudsql-oauth-credentials
        secret:
          secretName: cloudsql-oauth-credentials
      - name: ssl-certs
        hostPath:
          path: /etc/ssl/certs

完全なデプロイメントファイルは次のようになります。

    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
      name: jhipstergooglecloudsql
    spec:
      replicas: 1
      template:
        metadata:
          labels:
            app: jhipstergooglecloudsql
        spec:
          containers:
          - name: jhipstergooglecloudsql
            image: gcr.io/jhipster-kubernetes-cloud-sql/jhipstergooglecloudsql:v1
            env:
            - name: SPRING_PROFILES_ACTIVE
              value: prod
            - name: SPRING_DATASOURCE_URL
              value: jdbc:mysql://localhost:3306/jhipstergooglecloudsql?useUnicode=true&characterEncoding=utf8&useSSL=false
            ports:
            - containerPort: 8080
          - image: b.gcr.io/cloudsql-docker/gce-proxy:1.05
            name: cloudsql-proxy
            command: ["/cloud_sql_proxy", "--dir=/cloudsql",
                      "-instances=jhipster-kubernetes-cloud-sql:europe-west1:jhipster-sqlcloud-db=tcp:3306",
                      "-credential_file=/secrets/cloudsql/credentials.json"]
            volumeMounts:
              - name: cloudsql-oauth-credentials
                mountPath: /secrets/cloudsql
                readOnly: true
              - name: ssl-certs
                mountPath: /etc/ssl/certs
          volumes:
            - name: cloudsql-oauth-credentials
              secret:
                secretName: cloudsql-oauth-credentials
            - name: ssl-certs
              hostPath:
                path: /etc/ssl/certs


その後、`kubectl apply`を使用してクラスタをデプロイできます。

    kubectl apply -f jhipstergooglecloudsql

    deployment "jhipstergooglecloudsql" created
    service "jhipstergooglecloudsql" created


次に、`kubectl get services`を使用して外部IPを取得し、アプリケーションをテストできます。

    kubectl get services jhipstergooglecloudsql
    NAME                     CLUSTER-IP     EXTERNAL-IP     PORT(S)    AGE
    jhipstergooglecloudsql   10.95.251.18   104.199.51.11   8080/TCP   1m
