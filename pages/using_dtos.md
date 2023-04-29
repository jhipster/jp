---
layout: default
title: DTOの使用
permalink: /using-dtos/
redirect_from:
  - /using_dtos.html
sitemap:
    priority: 0.7
    lastmod: 2015-05-28T23:41:00-00:00
---

# <i class="fa fa-briefcase"></i> DTOの使用

## はじめに

デフォルトでは、JHipsterはドメイン・オブジェクト（通常はJPAエンティティ）をRESTエンドポイントで直接使用します。
これには多くの利点がありますが、主な利点は、コードに含まれるレイヤーが少ないため、コードが理解しやすいことです。

ただし、複雑なユースケースでは、RESTエンドポイントによって公開されるデータ転送オブジェクト（またはDTO）の使用を必要とする場合があります。これらのオブジェクトは、ドメインオブジェクトの上に追加のレイヤを追加し、特にRESTレイヤに合わせて調整されます：主な利点は、複数のドメインオブジェクトを集約できることです。

## JHipsterでのDTOの動作

JHipsterエンティティを生成する場合、サービスレイヤを追加するオプションがあります。DTOオプションは、マッピングを処理するためにサービスレイヤが必要なため、サービスレイヤを選択した場合にのみ使用できます（JPAを使用している場合、これはサービスレイヤがトランザクションであるため、遅延ロードが機能します）。

サービス・レイヤーを選択すると、エンティティのDTOを生成するオプションが表示されます。このオプションを選択すると、次のことが可能になります。

- DTOが生成され、元となるエンティティにマップされます。
- 多対1の関係を集約し、クライアント側のフレームワーク（Angularなど）で表示するために使用されるIDとフィールドのみを使用します。その結果、`User`エンティティへの多対1の関係は、`userId`フィールドと`userLogin`フィールドをDTOに追加します。
- 所有者でない側の1対多の関係と多対多の関係は無視します。これはエンティティの動作と一致します（エンティティはこれらのフィールドに`@JsonIgnore`アノテーションを持っています）。
- 所有者側の多対多関係の場合：他のエンティティからのDTOを`Set`で集約して使用します。これは、他のエンティティもDTOを使用する場合にのみ機能します。

## MapStructを使用したDTOとエンティティのマッピング

DTOはエンティティによく似ているため、DTOを互いに自動的にマッピングするソリューションが必要になることがよくあります。

JHipsterで選択されたソリューションは[MapStruct](http://mapstruct.org/)です。必要なマッピングを自動的に生成するのは、Javaコンパイラーにプラグインされたアノテーション・プロセッサーです。

非常にクリーンで効率的であり、リフレクションを使用しないことが気に入りました（リフレクションはマッパーのように多様するとパフォーマンスに悪影響を及ぼします）。

## MapStruct用にIDEを構成する

MapStructはアノテーションプロセッサであるため、IDEがプロジェクトをコンパイルするときに自動的に実行されるよう設定する必要があります。

Mavenを使用している場合は、IDEで`IDE`のMavenプロファイルをアクティブにする必要があります。Gradleユーザは、IDE固有のものを適用する必要はありません。

プロファイルをアクティブにする手順については、[IDEの設定]({{ site.url }}/configuring-ide/)を参照してください。

## 高度なMapStructの使用法

MapStructマッパーはSpring Beanとして構成され、依存性注入をサポートします。便利なヒントの1つは、マッパーに`Repository`を注入できるため、そのIDを使用してマッパーにて管理対象としたいJPAエンティティをフェッチできることです。

以下に`User`エンティティを取得するコードの例を示します。

    @Mapper
    public abstract class CarMapper {

        @Inject
        private UserRepository userRepository;

        @Mapping(source = "user.id", target = "userId")
        @Mapping(source = "user.login", target = "userLogin")
        public abstract CarDTO carToCarDTO(Car car);

        @Mapping(source = "userId", target = "user")
        public abstract Car carDTOToCar(CarDTO carDTO);

        public User userFromId(Long id) {
            if (id == null) {
                return null;
            }
            return userRepository.findOne(id);
        }
    }
