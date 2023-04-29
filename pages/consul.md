---
layout: default
title: Consul
permalink: /consul/
sitemap:
    priority: 0.7
    lastmod: 2017-05-03T00:00:00-00:00
---

# <i class="fa fa-bullseye"></i> Consul

## Consulの概観

JHipster Registryの代替として、Hashicorpのデータセンター管理ソリューションである[Consul](https://www.consul.io/)を使用することを選択できます。
Eurekaと比較すると、多くの利点があります。

- マルチノードクラスタでの操作は、Eurekaよりも簡単です。
- 可用性よりも一貫性を優先するため、クラスタの状態の変更がより迅速に伝播されます。
- Consulサービスディスカバリは、[DNSインターフェイス](https://www.consul.io/docs/agent/dns.html)または[HTTP API](https://www.consul.io/docs/agent/http.html)を介して既存のアプリケーションと相互運用できます。

## アーキテクチャ図

<img src="{{ site.url }}/images/microservices_architecture_detail.003.png" alt="Diagram" style="width: 800; height: 600" class="img-responsive"/>

## 入門

Consulレジストリに依存するアプリケーションの開発を開始するには、DockerコンテナでConsulインスタンスを起動します。

- `docker-compose -f src/main/docker/consul.yml up`を実行して、Consulサーバを`dev`モードで起動します。その後、ConsulはDockerホストのポート`8500`で使用可能になり、マシンで実行する場合は[http://127.0.0.1:8500/](http://127.0.0.1:8500/)となります。

[Docker Composeサブジェネレータ]({{ site.url }}/docker-compose/#docker-compose-subgen)を使用して、複数のConsul対応アプリケーションのDocker設定の生成もできます。

## Consulを使用したアプリケーション構成

JHipsterマイクロサービスまたはゲートウェイアプリケーションを生成するときにConsulオプションを選択した場合、Consulの**Key/Valueストア**から設定を取得するように自動的に設定されます。

Key/Value (K/V)ストアは、[http://localhost:8500/v1/kv/](http://localhost:8500/v1/kv/)または[REST API](https://www.consul.io/intro/getting-started/kv.html)で使用可能なUIを使用して変更できます。ただし、この方法で行われた変更は一時的なものであり、Consulサーバ/クラスタのシャットダウン時に失われます。
そのため、Key/Valueストアを操作し、YAMLファイルとして構成を管理するために、JHipsterチームは[consul-config-loader](https://github.com/jhipster/consul-config-loader)という小さなツールを開発しました。
**consul-config-loader**は、`consul.yml`docker-composeファイルからConsulを起動するときに自動的に設定されますが、スタンドアローンツールとしての実行もできます。
次の2つのモードで実行できます。

- **dev**モードでは、`central-server-config`ディレクトリのYAMLファイルが自動的にConsulにロードされます。さらに、このディレクトリに対する変更はすべて、すぐにConsulと同期されます。
- **prod**モードでは、Git2Consulを使用して、Gitリポジトリに含まれるYAMLファイルをKey/Valueストアの設定ソースとして設定します。

JHipsterレジストリと同様に、構成ファイルには`appname-profile.yml`という名前を付ける必要があります。ここで、appnameとprofileは、構成するサービスのアプリケーション名とプロファイルに対応します。たとえば、`consulapp-prod.yml`ファイルにプロパティを追加すると、これらのプロパティは、`prod`プロファイルで開始された`consulapp`という名前のアプリケーションに対してのみ設定されます。さらに、`application.yml`で定義されたプロパティは、すべてのアプリケーションに対して設定されます。
