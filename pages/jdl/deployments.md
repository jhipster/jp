---
layout: default
title: JHipsterドメイン言語 - デプロイメント
permalink: /jdl/deployments
sitemap:
    priority: 0.5
    lastmod: 2021-07-08T12:00:00-00:00
---

# <i class="fa fa-star"></i> JHipsterドメイン言語(JDL) - デプロイメント

## 概要

1. [構文](#構文)
1. [例](#例)
1. [使用可能なデプロイメントのオプション](#使用可能なデプロイメントのオプション)

---

### 構文

デプロイメント宣言は次のように行われます。

```
deployment {
  <デプロイメントオプション名> <デプロイメントオプション値>
}
```

  - アプリケーションと同様に、オプションのキーと値を指定することでデプロイメント宣言が機能します。

---

### 例

#### 基本の例

```jdl
deployment {
  deploymentType docker-compose
  appsFolders [foo, bar]
  dockerRepositoryName "yourDockerLoginName"
}
```

---

#### 複数のデプロイメント

複数のデプロイメントが必要な場合は、次のようにします。

```
// 'docker-compose'フォルダの下に作成されます
deployment {
  deploymentType docker-compose
  appsFolders [foo, bar]
  dockerRepositoryName "yourDockerLoginName"
}

// 'kubernetes'フォルダの下に作成されます
deployment {
  deploymentType kubernetes
  appsFolders [foo, bar]
  dockerRepositoryName "yourDockerLoginName"
}
```

`deploymentType`ごとに1つの配置を持つことができます。`appsFolders`で定義されたアプリケーションは、デプロイメントを作成するフォルダと同じフォルダ、または`directoryPath`
で定義されたフォルダにある必要があります。

たとえば、上記では、次のようなフォルダ構造が必要です。

```
.
├── yourJdlFile.jdl
├── foo
├── bar
├── kubernetes // JDLによって作成されます
└── docker-compose // JDLによって作成されます
```

---

### 使用可能なデプロイメントのオプション

JDLでサポートされているデプロイメントオプションは次のとおりです。

<table class="table table-striped table-responsive">
  <tr>
    <th>JDLオプション名</th>
    <th>デフォルト値</th>
    <th>指定可能な値</th>
    <th>コメント</th>
  </tr>
  <tr>
    <td>deploymentType</td>
    <td>docker-compose</td>
    <td>docker-compose, kubernetes, openshift</td>
    <td></td>
  </tr>
  <tr>
    <td>directoryPath</td>
    <td>"../"</td>
    <td></td>
    <td>相対パス。二重引用符で囲む必要があります</td>
  </tr>
  <tr>
    <td>appsFolders</td>
    <td>[]</td>
    <td></td>
    <td>アプリケーションのディレクトリ名。カンマで区切られたリストである必要があります。例:[foo, bar]</td>
  </tr>
  <tr>
    <td>clusteredDbApps</td>
    <td>[]</td>
    <td></td>
    <td>クラスタ化されたDBを持つアプリケーションのディレクトリ名。カンマで区切られたリストである必要があります。例:[foo, bar]</td>
  </tr>
  <tr>
    <td>gatewayType</td>
    <td>SpringCloudGateway</td>
    <td>serviceDiscoveryTypeが`no`の場合、値は無視されます</td>
  </tr>
  <tr>
    <td>monitoring</td>
    <td>no</td>
    <td>no, prometheus</td>
    <td></td>
  </tr>
  <tr>
    <td>serviceDiscoveryType</td>
    <td>eureka</td>
    <td>eureka, consul, no</td>
    <td></td>
  </tr>
  <tr>
    <td>dockerRepositoryName</td>
    <td></td>
    <td></td>
    <td>Dockerリポジトリの名前またはURL。二重引用符で囲む必要があります</td>
  </tr>
  <tr>
    <td>dockerPushCommand</td>
    <td>"docker push"</td>
    <td></td>
    <td>使用するdocker pushコマンド。二重引用符で囲む必要があります</td>
  </tr>
  <tr>
    <td>kubernetesNamespace</td>
    <td>default</td>
    <td></td>
    <td>deploymentTypeがkubernetesの場合にのみ適用可能</td>
  </tr>
  <tr>
    <td>kubernetesUseDynamicStorage</td>
    <td>false</td>
    <td>true, false</td>
    <td>deploymentTypeがkubernetesの場合にのみ適用され、kubernetesStorageClassNameオプションが有効になります</td>
  </tr>
  <tr>
    <td>kubernetesStorageClassName</td>
    <td>""</td>
    <td></td>
    <td>deploymentTypeがkubernetesの場合にのみ適用されます。空のままにすることができます(2つの二重引用符)</td>
  </tr>
  <tr>
    <td>kubernetesServiceType</td>
    <td>LoadBalancer</td>
    <td>LoadBalancer, NodePort, Ingress</td>
    <td>deploymentTypeがkubernetesの場合にのみ適用可能</td>
  </tr>
  <tr>
    <td>ingressDomain</td>
    <td></td>
    <td></td>
    <td>kubernetesServiceTypeが`Ingress`の場合のIngressのドメイン。二重引用符で囲む必要があります。deploymentTypeがkubernetesの場合にのみ適用されます。</td>
  </tr>
  <tr>
    <td>ingressType</td>
    <td>nginx</td>
    <td>nginx, gke</td>
    <td>kubernetesのIngressタイプ。`kubernetesServiceType`がIngressに設定されている場合にのみ設定されます。</td>
  </tr>
  <tr>
    <td>istio</td>
    <td>false</td>
    <td>true, false</td>
    <td>deploymentTypeがkubernetesの場合にのみ適用可能</td>
  </tr>
  <tr>
    <td>openshiftNamespace</td>
    <td>default</td>
    <td></td>
    <td>deploymentTypeがopenshiftの場合にのみ適用可能</td>
  </tr>
  <tr>
    <td>storageType</td>
    <td>ephemeral</td>
    <td>ephemeral, persistent</td>
    <td>deploymentTypeがopenshiftの場合にのみ適用可能</td>
  </tr>
  <tr>
    <td>registryReplicas</td>
    <td>2</td>
    <td></td>
    <td>レプリカの数(deploymentTypeがopenshiftの場合)</td>
  </tr>
</table>
