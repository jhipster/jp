---
layout: default
title: JHipsterドメイン言語 - オプション
permalink: /jdl/options
sitemap:
    priority: 0.5
    lastmod: 2019-11-02T12:00:00-00:00
---

# <i class="fa fa-star"></i> JHipsterドメイン言語(JDL) - オプション

## 概要

JHipsterでは、ページ区切りやDTOなどのエンティティのオプションを指定できます。
JDLでは、エンティティのアノテーションまたは次の構文を使用して、同じ操作ができます。

    entity A {
      name String required
    }
    entity B
    entity C

    dto A, B with mapstruct

    paginate A with infinite-scroll
    paginate B with pagination
    paginate C with pager  // pagerはAngularJSでのみ利用可能

    service A with serviceClass
    service C with serviceImpl

使用可能なオプションの完全なリストは、[こちら](#使用可能なオプション)にあります。

1. [操作方法](#操作方法)
1. [構文](#構文)
1. [XYZオプションを使用](#xyzオプションを使用)
1. [例](#例)
   1. [基本の単項の例](#基本の単項の例)
   1. [基本の二項の例](#基本の二項の例)
   1. [all, * の例](#all--の例)
   1. [all, * の除外の例（単項）](#all--の除外の例単項)
   1. [all, * の除外の例（二項）](#all--の除外の例二項)
   1. [カスタム値を持つオプション](#カスタム値を持つオプション)
   1. [混在する例](#混在する例)
1. [サービスについて](#サービスについて)
1. [マイクロサービス関連のオプション](#マイクロサービス関連のオプション)
1. [カスタム・アノテーション](#カスタムアノテーション)
1. [使用可能なオプション](#使用可能なオプション)
1. [関連項目](#関連項目)

---

### 操作方法

次の2種類のオプションがあります。
  - 単項（オプション値なし）
  - 二項（値付き）

エンティティにオプションを適用するには、次の3つの方法があります。
  - オプション名（`dto`, `readOnly`など）の使用。例を参照してください。
  - アノテーションの使用
  - `use XYZ`形式を使用

これらを混在させると読みにくくなるため、お勧めしません。

---

### 構文

通常のフォームの場合は以下です。
```
<オプション名> <エンティティリスト>

または

<オプション名> <エンティティリスト> with <オプション値>

または

<オプション名> <エンティティリスト> with <オプション値> except <除外エンティティリスト>

または 

<オプション名> <エンティティリスト> except <除外エンティティリスト>
```

  - 単項オプションの場合
    - オプション名とリストが必要です。
    - 除外されるエンティティはオプションで`except`キーワードを付けます（詳細は以下を参照してください）。
  - 二項オプションの場合
    - エンティティリストは、`with`キーワードおよびオプション値の前に配置されます。
    - ここでも、除外されるエンティティは最後に`except`キーワードを付けます。

アノテーションは以下です。
```
@<オプション名>
entity <エンティティ名>

または

@<オプション名>(<オプション値>)
```

  - Javaと同様に、アノテーションは括弧内の値を取ることができます。
    - オプションに応じて、値はオプションになる場合とならない場合があります。

---

### XYZオプションを使用

useオプション形式で、エンティティーにいくつかのオプションを指定できます。
これはJHipster Code 2020で作成されたもので、その作成理由は次のとおりです。
  - オプションを無効にする課題を解決します（JHipsterには'no'を示す方法が複数あります：`no, false, none`）
  - エンティティごとにオプションをグループ化する方法を提示できます

```jdl
entity A
entity B
entity C

use serviceClass for * except C
use mapstruct, serviceImpl, infinite-scroll for A, B
use pagination for C
```

<table class="table table-striped table-responsive">
  <tr>
    <th>useオプションの値</th>
    <th>コメント</th>
  </tr>
  <tr>
    <td>mapstruct</td>
    <td>エンティティのDTOを作成するかどうか。エンティティにDTOがあってもサービスがない場合は、'serviceClassが使用されます'</td>
  </tr>
  <tr>
    <td>serviceClass</td>
    <td></td>
  </tr>
  <tr>
    <td>serviceImpl</td>
    <td></td>
  </tr>
  <tr>
    <td>pagination</td>
    <td>アプリケーションがCassandraを使用する場合、オプションとしてのページ区切りは禁止です</td>
  </tr>
  <tr>
    <td>infinite-scroll</td>
    <td>アプリケーションがCassandraを使用する場合、オプションとしてのページ区切りは禁止です</td>
  </tr>
  <tr>
    <td>elasticsearch</td>
    <td>アプリケーションでsearchEngineオプションを有効にする必要があります</td>
  </tr>
  <tr>
    <td>couchbase</td>
    <td>アプリケーションでsearchEngineオプションを有効にする必要があります</td>
  </tr>
</table>

---

### 例

各例には、次の3つの形式があります。
  - 標準形式
  - アノテーションベースの形式
  - use形式（該当する場合）

---

#### 基本の単項の例

標準形式：
```jdl
entity A

readOnly A
```

アノテーションベース形式：
```jdl
@readOnly
entity A
```

---

#### 基本の二項の例

標準形式：
```jdl
entity A

dto A with mapstruct
```

アノテーション形式：
```jdl
@dto(mapstruct)
entity A
```

`use`キーワードの使用：
```jdl
entity A

use mapstruct, serviceImpl, pagination for A
```

---

#### all, * の例

`all` と `*` はエイリアスです。

標準形式：
```jdl
entity A
entity B

dto all with mapstruct
```

アノテーション形式：
```jdl
@dto(mapstruct)
entity A

@dto(mapstruct)
entity B
```

`use`キーワードの使用：
```jdl
entity A
entity B

use mapstruct, serviceImpl, pagination for *
```

---

#### all, * の除外の例（単項）

標準形式：
```jdl
entity A
entity B

skipClient * except A
```

アノテーション形式：
```jdl
entity A

@skipClient
entity B
```

`use`キーワードの使用：
```jdl
entity A
entity B

use mapstruct, serviceImpl, pagination for * except A
```

---

#### all, * の除外の例（二項）

標準形式：
```jdl
entity A
entity B

dto all with mapstruct except A
```

アノテーション形式：
```jdl
entity A

@dto(mapstruct)
entity B
```

`use`キーワードの使用：
```jdl
entity A
entity B

use mapstruct, serviceImpl, pagination for all except A
```

---

#### カスタム値を持つオプション

```jdl
entity A
entity B

microservice all with mySuperMS
```

---

#### 混在する例

標準形式：
```jdl
entity A
entity B
entity C

readOnly B, C
dto * with mapstruct except C
service * with serviceClass except C
search A with elasticsearch
```

アノテーション形式：
```jdl
@dto(mapstruct)
@search(elastisearch)
@service(serviceClass)
entity A

@readOnly
@dto(mapstruct)
@service(serviceClass)
entity B

@readOnly
entity C
```

---

### サービスについて

サービスの指定がない場合、リポジトリインタフェースを直接呼び出すリソースクラスが作成されます。これは
デフォルトで最も単純なオプションです（Aを参照）。

`service with serviceClass`（Bを参照）は、リポジトリインタフェースを呼び出すサービスクラスをリソースが呼び出すようにします。
`service with serviceImpl`（Cを参照）は、リソースクラスによって使用されるサービスインタフェースを作成します。

このインタフェースは、リポジトリー・インタフェースを呼び出す具象クラスによって実装されます。

確実でない限りサービスを使用しないことは、最も簡単なオプションであり、CRUDに適しています。クラスでサービスを使用するのは
複数のリポジトリを使用するビジネスロジックのため、サービスクラスに最適です。JHipsterの開発者陣は
不要なインタフェースを好みません。しかし、気に入ったのであれば、implを使ってサービスを利用してください。

    entity A
    entity B
    entity C

    // Aに対応するサービスは無し
    service B with serviceClass
    service C with serviceImpl

---

### マイクロサービス関連のオプション

JHipster v3では、マイクロサービスを作成できます。JDLでエンティティを生成するためのいくつかのオプションを指定できます。
マイクロサービスの名前と検索エンジンです。

マイクロサービスの名前（JHipsterアプリの名前）を指定する方法を次に示します。

```
entity A
entity B
entity C
microservice * with mysuperjhipsterapp except C
microservice C with myotherjhipsterapp
search * with elasticsearch except C
```

最初のオプションは、マイクロサービスにエンティティを処理させたいことをJHipsterに伝えるために使用され、2番目のオプションは
エンティティの検索方法とエンティティを検索対象とするかどうかを指定します。

---

### カスタム・アノテーション

JDLでは、次のようなカスタムアノテーションが可能です。

```jdl
@customAnnotation(customValue)
entity A
```

これの主なユースケースはBlueprintです。場合によっては、エンティティやフィールドのカスタムオプションが必要になることもあります。
通常のオプション（`dto`, `pagination`など）の場合、これらのオプションはCLIと同様にJSONで生成されます。
ただし、カスタムオプションの場合は、ダンプされたJSONの`options`キーの下に生成されます。

---

### 使用可能なオプション

JDLでサポートされているエンティティオプションは次のとおりです。

_あなたが探しているものではありませんか?[アプリケーションのオプション](/jdl/applications#available-application-configuration-options)をチェックしてください。_

<table class="table table-striped table-responsive">
  <tr>
    <th>JDLオプション名</th>
    <th>オプションタイプ</th>
    <th>デフォルト値</th>
    <th>指定可能な値</th>
    <th>コメント</th>
  </tr>
  <tr>
    <td>skipClient</td>
    <td>unary</td>
    <td>false</td>
    <td></td>
    <td>これにより、クライアントコードの生成がスキップされます。</td>
  </tr>
  <tr>
    <td>skipServer</td>
    <td>unary</td>
    <td>false</td>
    <td></td>
    <td>これにより、サーバ・コードの生成がスキップされます</td>
  </tr>
  <tr>
    <td>noFluentMethod</td>
    <td>unary</td>
    <td>false</td>
    <td></td>
    <td>
      詳細は<a href="https://www.jhipster.tech/2016/08/17/jhipster-release-3.6.0.html#important-change-fluent-setters">このメモ</a>
      を参照してください。
    </td>
  </tr>
  <tr>
    <td>filter</td>
    <td>unary</td>
    <td>false</td>
    <td></td>
    <td>
      詳細は<a href="https://www.jhipster.tech/entities-filtering/">フィルタリング</a>を参照してください。もしエンティティがフィルタされていても
      サービスがない場合は、'serviceClass'が使用されます。
    </td>
  </tr>
  <tr>
    <td>readOnly</td>
    <td>unary</td>
    <td>false</td>
    <td></td>
    <td>
      このオプションを追加すると、エンティティがreadOnlyになります。
      詳細は<a href="https://www.jhipster.tech/2019/10/10/jhipster-release-6.4.0.html#jhipster-release-v640">このリリースノート</a>
      を参照してください。
     </td>
  </tr>
  <tr>
    <td>dto</td>
    <td>binary</td>
    <td>no</td>
    <td>mapstruct, no</td>
    <td>エンティティのDTOを作成するかどうか。エンティティにDTOがあってもサービスがない場合は、'serviceClass'が使用されます。</td>
  </tr>
  <tr>
    <td>service</td>
    <td>binary</td>
    <td>no</td>
    <td>serviceClass, serviceImpl, no</td>
    <td></td>
  </tr>
  <tr>
    <td>paginate</td>
    <td>binary</td>
    <td>no</td>
    <td>pagination, infinite-scroll, no</td>
    <td>アプリケーションがCassandraを使用している場合、ページ付けは禁止です</td>
  </tr>
  <tr>
    <td>search</td>
    <td>binary</td>
    <td>no</td>
    <td>elasticsearch, no</td>
    <td>アプリケーションでsearchEngineオプションを有効にする必要があります</td>
  </tr>
  <tr>
    <td>microservice</td>
    <td>binary</td>
    <td></td>
    <td>custom value</td>
    <td>マイクロサービスアプリケーション内で宣言されたすべてのエンティティに自動的に追加されます</td>
  </tr>
  <tr>
    <td>angularSuffix</td>
    <td>binary</td>
    <td></td>
    <td>カスタム値</td>
    <td></td>
  </tr>
  <tr>
    <td>clientRootFolder</td>
    <td>binary</td>
    <td></td>
    <td>カスタム値</td>
    <td></td>
  </tr>
</table>

---

### 関連項目

アプリケーションのオプションは、[ここ](/jdl/applications)にあります。
