---
layout: default
title: 共通アプリケーションプロパティ
permalink: /common-application-properties/
sitemap:
    priority: 0.7
    lastmod: 2018-03-18T18:20:00-00:00
---

# <i class="fa fa-flask"></i> 共通アプリケーションプロパティ

JHipsterはSpring Bootアプリケーションを生成し、標準のSpring Bootプロパティの仕組みを使用して設定できます。

これらのプロパティはJHipsterによって生成時に設定され、開発モードとプロダクションモードでは値が異なることがよくあります。詳細については、[プロファイルのドキュメント]({{ site.url }}/profiles/)を参照してください。

JHipsterアプリケーションには、次の3種類のプロパティがあります。

1. [Spring Boot標準アプリケーションプロパティ](#1)
2. [JHipsterアプリケーションプロパティ](#2)
3. [アプリケーション固有のプロパティ](#3)

<h2 id="1">Spring Boot標準アプリケーションプロパティ</h2>

他のSpring Bootアプリケーションと同様に、JHipsterでは標準の[Spring Bootアプリケーションプロパティ](http://docs.spring.io/spring-boot/docs/current/reference/html/common-application-properties.html)を設定できます。

<h2 id="2">JHipsterアプリケーションプロパティ</h2>

JHipsterは、[JHipsterサーバサイドライブラリ](https://github.com/jhipster/jhipster)からなる固有のアプリケーションプロパティを提供します。これらのプロパティはすべてのJHipsterプロジェクトで標準ですが、アプリケーションを構築したときに選択した内容に応じてのみ機能するものもあります。たとえば、`jhipster.cache.hazelcast`キーは、第2レベルのHibernateキャッシュとしてHazelcastを選択した場合にのみ機能します。

これらのプロパティは、`io.github.jhipster.config.JHipsterProperties`クラスを使用して設定されます。

これらのプロパティのドキュメントを次に示します。

```YAML
    jhipster:

        # JHipsterの非同期メソッド呼び出しに使用されるスレッドプール
        async:
            core-pool-size: 2 # 初期プール・サイズ
            max-pool-size: 50 # 最大プール・サイズ
            queue-capacity: 10000 # プールのキュー容量

        # JHipsterゲートウェイの特定の設定
        # JHipsterゲートウェイの詳細についてはhttps://www.jhipster.tech/api-gateway/を参照
        gateway:
            rate-limiting:
                enabled: false # レート制限は、デフォルトでは無効
                limit: 100_000L # デフォルトでは、100,000のAPIコールが許可
                duration-in-seconds: 3_600 # デフォルトでは、レート制限は1時間ごとに再初期化
            authorized-microservices-endpoints: # アクセスコントロールポリシー。ルートに対して空のままにしておくと、すべてのエンドポイントがアクセス可能になります。
                app1: /api # プロダクション設定の推奨。"app1"マイクロサービスからのすべてのAPIコールへのアクセスを許可します。

        # HTTP設定
        http:
            cache: # io.github.jhipster.web.filter.CachingHttpHeadersFilterより使用
                timeToLiveInDays: 1461 # 静的なアセットはデフォルトで4年間キャッシュ

        # Hibernateの第2レベルのキャッシュ（CacheConfigurationで使用）
        cache:
            hazelcast: # Hazelcastの設定
                time-to-live-seconds: 3600 # デフォルトでは、オブジェクトはキャッシュに1時間保持
                backup-count: 1 # オブジェクトのバックアップ数
                # Hazelcast管理センターの設定
                # 完全なリファレンスは、http://docs.hazelcast.org/docs/management-center/3.9/manual/html/Deploying_and_Starting.htmlにあります。
                management-center:
                    enabled: false # Hazelcast管理センターはデフォルトで無効
                    update-interval: 3 # アップデートはデフォルトで3秒ごとにHazelcast管理センターに送信
                    # JHipsterのDocker Compose設定を使用する場合のHazelcast管理センターのデフォルトURL
                    # src/main/docker/hazelcast-management-center.ymlを参照
                    # 注意：ポート8080はすでにJHipsterによって使用されているため、デフォルトのポートは8180
                    url: http://localhost:8180/mancenter
            ehcache: # Ehcacheの設定
                time-to-live-seconds: 3600 # デフォルトでは、オブジェクトはキャッシュに1時間保持
                max-entries: 100 # 各キャッシュ・エントリ内のオブジェクト数
            caffeine: # Caffeineの設定
                time-to-live-seconds: 3600 # デフォルトでは、オブジェクトはキャッシュに1時間保持
                max-entries: 100 # 各キャッシュ・エントリ内のオブジェクト数
            infinispan: #Infinispanの設定
                config-file: default-configs/default-jgroups-tcp.xml
                # ローカルアプリケーションキャッシュ
                local:
                    time-to-live-seconds: 60 # デフォルトでは、オブジェクトはキャッシュに1時間(分単位)保持
                    max-entries: 100 # 各キャッシュ・エントリ内のオブジェクト数
                #distributed app cache
                distributed:
                    time-to-live-seconds: 60 # デフォルトでは、オブジェクトはキャッシュに1時間(分単位)保持
                    max-entries: 100 # 各キャッシュ・エントリ内のオブジェクト数
                    instance-count: 1
                #replicated app cache
                replicated:
                    time-to-live-seconds: 60 # デフォルトでは、オブジェクトはキャッシュに1時間(分単位)保持
                    max-entries: 100 # 各キャッシュ・エントリ内のオブジェクト数
            # Memcachedの設定
            # Xmemcachedライブラリを使用。https://github.com/killme2008/xmemcachedを参照
            memcached:
                # Spring Boot devtoolsで動作しないため、開発モードではデフォルトで無効
                enabled: true
                servers: localhost:11211 # コンマまたは空白で区切られたサーバーのアドレスのリスト
                expiration: 300 # キャッシュの有効期限(秒単位)
                use-binary-protocol: true # バイナリプロトコルが推奨。パフォーマンス（およびセキュリティ）のため
                authentication: # 認証が必要な場合は、次のパラメータを使用して設定できます。デフォルトでは無効。
                    enabled: false,
                    # username: デフォルトでは設定なし
                    # password: デフォルトでは設定なし
            redis: # Redisの設定
                expiration: 3600 # デフォルトでは、オブジェクトはキャッシュに1時間(秒単位)保持
                server: redis://localhost:6379 # サーバアドレス
                cluster: false
                connectionPoolSize: 64,
                connectionMinimumIdleSize: 24,
                subscriptionConnectionPoolSize: 50,
                subscriptionConnectionMinimumIdleSize: 1

        # E-mailプロパティ
        mail:
            enabled: false # 電子メールの送信が有効になっている場合、標準の`spring.mail`キーを設定する必要があります
            from: jhipster@localhost # 電子メールのデフォルトの送信元アドレス
            base-url: http://127.0.0.1:8080 # 電子メール内で使用されるアプリケーションのURL

        # Spring Security固有の設定
        security:
            remember-me: # remember-meメカニズムのJHipsterセキュア実装。セッションベースの認証用
                # セキュリティキー（このキーは、アプリケーションに固有で、秘密にしておく必要があります）
                key: 0b32a651e6a65d5731e869dc136fb301b0a8c0e4
            authentication:
                jwt: # JHipster固有のJWT実装
                    # シークレットトークンはBase64を使ってエンコードされるべきです（コマンドラインで`echo 'secret-key'|base64`とタイプできます）。
                    # 両方のプロパティが設定されている場合、`secret`プロパティは`base64-secret`プロパティよりも優先順位が高くなります。
                    secret: # クリア・テキストのJWT秘密鍵（推奨されません）
                    base64-secret:  # Base64でエンコードされたJWT秘密鍵（推奨）
                    token-validity-in-seconds: 86400 # トークンは24時間有効
                    token-validity-in-seconds-for-remember-me: 2592000 # Remember meトークンは30日間有効

        # Swagger設定
        swagger:
            default-include-pattern: /api/.*
            title: JHipster API
            description: JHipster API documentation
            version: 0.0.1
            terms-of-service-url:
            contact-name:
            contact-url:
            contact-email:
            license:
            license-url:
            host:
            protocols:

        # DropWizard Metrics設定。MetricsConfigurationで使用します。
        metrics:
            jmx: # メトリックをJMX Beanとしてエクスポート
                enabled: true # JMXはデフォルトで有効
            # Graphiteサーバーにメトリックを送信します。
            # "graphite" Mavenプロファイルを使用。Graphiteとの依存関係をもちます。
            graphite:
                enabled: false # Graphiteはデフォルトで無効
                host: localhost
                port: 2003
                prefix: jhipster
            # Prometheusサーバにメトリックを送信します。
            prometheus:
                enabled: false # Prometheusはデフォルトで無効
                endpoint: /prometheusMetrics
            logs: # ログ内のDropwizardメトリックをレポート
                enabled: false
                reportFrequency: 60 # 秒単位のレポートの頻度

        # ロギング設定。LoggingConfigurationで使用
        logging:
            logstash: # ソケット経由でLogstashにログを転送する
                enabled: false # Logstashはデフォルトで無効
                host: localhost # LogstashサーバーURL
                port: 5000 # Logstashサーバーポート
                queue-size: 512 # ログをバッファリングするためのキュー
            spectator-metrics: # ログ内のNetflix Spectatorメトリクスをレポート
                enabled: false # Spectatorはデフォルトで無効

        # デフォルトでは、cross-origin resource sharing (CORS) は、モノリスおよびゲートウェイの"dev" モードで
        # 有効になっています。
        # セキュリティ上の理由から、"prod"モードではデフォルトで無効になっています。マイクロサービスの場合も同様です
        # (アクセスにはゲートウェイを使用することを想定）。
        # これにより、標準のorg.springframework.web.cors.CorsConfigurationが設定されます。
        # "exposed-headers" がJWTベースのセキュリティーでは必須であることに注意してください。
        # "Authorization"ヘッダーを使用し、デフォルトの公開ヘッダーではありません。
        cors:
            allowed-origins: "*"
            allowed-methods: "*"
            allowed-headers: "*"
            exposed-headers: "Authorization"
            allow-credentials: true
            max-age: 1800

        # JHipsterアプリケーションの左上に表示されるリボン
        ribbon:
            # リボンを表示するプロファイルのカンマ区切りのリスト
            display-on-active-profiles: dev
```

<h2 id="3">アプリケーション固有のプロパティ</h2>

生成されたアプリケーションは、独自のSpring Bootプロパティを持つこともできます。これは、アプリケーションのタイプセーフな設定と、IDE内でのオートコンプリートとドキュメント化を可能にするため、強く推奨されます。

JHipsterは、`config`パッケージに`ApplicationProperties`クラスを生成しました。このクラスはすでに事前設定されており、`application.yml`、`application-dev.yml`、`application-prod.yml`ファイルの下部に文書化されています。必要なのは、独自の特定のプロパティをコーディングすることだけです。
