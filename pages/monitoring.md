---
layout: default
title: JHipsterアプリケーションのモニタリング
permalink: /monitoring/
sitemap:
    priority: 0.7
    lastmod: 2021-11-05T00:00:00-00:00
---
# <i class="fa fa-line-chart"></i> JHipsterアプリケーションのモニタリング

JHipsterには、実行時にアプリケーションをモニタリングするためのオプションがいくつか用意されています。

## サマリー

1. [生成されたダッシュボード](#generated-dashboards)
2. [セキュリティメトリック](#security-metrics)
3. [JHipsterレジストリ](#jhipster-registry)
4. [ELK](#elk)
5. [サポートされているサードパーティモニタリングシステムへのメトリックの転送](#configuring-metrics-forwarding)
6. [Zipkin](#zipkin)

## 生成されたダッシュボード

モノリスとゲートウェイの場合、JHipsterは各アプリケーションを監視するための複数のダッシュボードを生成します。
これらのダッシュボードは実行時に使用可能であり、監視を行うための最も簡単な方法です。

![JHipster Metrics page][jhipster-metrics-page]

### 集計ダッシュボード

メトリクスダッシュボードは、Micrometerを使用して、アプリケーションパフォーマンスの詳細なビューを提供します。

次のメトリックが表示されます。

- JVM
- HTTPリクエスト
- キャッシュの使用状況
- データベース接続プール

JVMスレッド・メトリックの横にあるExpandボタンをクリックすると、実行中のアプリケーションのスレッド・ダンプが表示されます。これは、ブロックされているスレッドを見つけるのに非常に役立ちます。

### ヘルスダッシュボード

ヘルスダッシュボードは、Spring Boot Actuatorのヘルスエンドポイントを使用して、アプリケーションのさまざまな部分のヘルス情報を提供します。多くのヘルスチェックは、Spring Boot Actuatorによってすぐに提供され、アプリケーション固有のヘルスチェックの追加もできます。

### ログダッシュボード

ログダッシュボードを使用すると、実行中のアプリケーションのLogback設定を実行時に管理できます。
Javaパッケージのログ・レベルを変更するには、ボタンをクリックします。これは、開発環境とプロダクション番環境の両方で非常に便利です。

## セキュリティ・メトリック
JHipsterは、JWT認証タイプを使用するプロジェクトのJWT関連のセキュリティメトリックを追跡します。

特に、JHipsterは、トークン検証エラー数（無効なトークン数）を`security.authentication.invalid-tokens`という名前のカスタムメーターとして追跡し、次のメータータグを使用してそのような検証エラーの原因を追跡します。
- `invalid-signature`:JWT署名の検証に失敗しました。
- `expired`:JWTの有効期限が切れています。
- `unsupported`:JWTフォーマットがアプリケーションで想定されているフォーマットと一致しません。
- `malformed`:JWTが正しく構築されていません。

これらのメトリックは生成されたダッシュボードでは使用できませんが、アプリケーションメトリックとして公開され、可視化のために[サードパーティの監視システムに転送](#configuring-metrics-forwarding)できます。

## JHipsterレジストリ

JHipster Registryには[こちらに独自のドキュメントページ]({{ site.url }}/jhipster-registry/)があります。

ほとんどの場合、前のセクションと同じ監視ダッシュボードが提供されますが、別のサーバで動作します。そのため、設定が少し複雑になりますが、実行中のアプリケーションの外部でダッシュボードを実行することを強くお勧めします。そうしないと、アプリケーションエラーが発生したときにダッシュボードを使用できなくなります。

<h2 id="elk">ELK (Elasticsearch, Logstash, Kibana)スタック</h2>

ELKスタックは、ログの集約と検索によく使用され、次のコンポーネントで構成されています。


- [Elasticsearch](https://www.elastic.co/products/elasticsearch)：データ（ログとメトリック）のインデックス作成
- [Logstash](https://www.elastic.co/products/logstash)：アプリケーションから受信したログを管理および処理
- [Kibana](https://www.elastic.co/products/kibana)：ログを可視化するための優れたインタフェース

<div class="alert alert-warning"><i>警告:</i>
JHipsterはLogstashへのログの転送をサポートしていますが、JHipsterバージョン7では、ELKスタックDockerデプロイメントは提供されておらず、ダッシュボードを使用する準備ができていません。これは、現在は保守されていない<a href="https://github.com/jhipster/jhipster-console">JHipsterコンソール</a>サブプロジェクトの一部でした。既存のユーザーには、別のELKソリューションに移行することをお勧めします。</div>


### Logstashへのログの転送

ログをLogstashに転送するようにJHipsterアプリケーションを構成するには、`application-dev.yml`または`application-prod.yml`でlogstashロギングを有効にします。

    jhipster:
        logging:
            logstash:
                enabled: true
                host: localhost
                port: 5000
                queueSize: 512

これらのログを収集するには、Logstash側で簡単な`logstash.conf`ファイルを用意します。

    input {
        tcp {
            port => "5000"
            type => syslog
            codec => json_lines
        }
    }

    output {
        elasticsearch {
                hosts => ["${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT}"]
                index => "logs-%{+YYYY.MM.dd}"
            }
        }
    }

ELKスタックのセットアップ方法の詳細については、[公式Elasticドキュメント](https://www.elastic.co/guide/en/elastic-stack/current/index.html)を参照してください。

<h2 id="configuring-metrics-forwarding">サポートされているサードパーティ監視システム(JMX、Prometheus)へのメトリックの転送</h2>

JHipsterは、デフォルトで[Prometheus](https://prometheus.io/)フォーマットのアプリケーションメトリックを公開します。
`management/prometheus`の下で公開されます。
代替システムへのメトリックの転送は、[spring boot actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-features.html#production-ready-metrics)を介してもサポートされています。

メトリックエンドポイントの公開を無効にしたい場合は、`src/main/resources/application.yml`で無効にできます。

    management:
        metrics:
            export:
                prometheus:
                    enabled: false


prometheusエンドポイントはデフォルトでは保護されていません。Spring Security経由で保護したい場合は、prometheusがベーシック認証で保護されたスクレイピングエンドポイントにおいて動作するように、prometheusエンドポイントにベーシック認証を追加することで保護できます。

新しい設定ファイル（例：`BasicAuthConfiguration.java`）を作成します。

    @Configuration
    @Order(1)
    @ConditionalOnProperty(prefix = "management", name = "metrics.export.prometheus.enabled")
    public class BasicAuthConfiguration {

        @Bean
        public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
            http
                .antMatcher("/management/prometheus/**")
                .authorizeRequests()
                .anyRequest().hasAuthority(AuthoritiesConstants.ADMIN)
                .and()
                .httpBasic().realmName("jhipster")
                .and()
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and().csrf().disable();
            return http.build();
        }
    }


デフォルトの`admin/admin`でログインできます。prometheusがアプリケーションをスクレイピングできるように、次の設定をprometheus設定に追加する必要があります。

    basic_auth:
        username: "admin"
        password: "admin"

`docker-compose -f src/main/docker/monitoring.yml up -d`を使用して、ローカルマシン上で事前設定されたGrafanaとPrometheusのインスタンスを起動し、
[jvm/micrometer dashboard](https://grafana.com/grafana/dashboards/4701)を参照してください。

![Grafana Micrometer Dashboard][grafana-micrometer-dashboard]

注：以前のJHipsterバージョンとは異なり、JHipster 5.8のメトリックレポートは、JMXとPrometheusのみをサポートしています。[Graphite](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-features.html#production-ready-metrics-export-graphite)のような他のレポーターを設定する方法については、Metricsの公式ドキュメントを参照してください。

## Zipkin

JHipsterアプリケーションは、[Spring Cloud Sleuth](https://cloud.spring.io/spring-cloud-sleuth/)を通して[Zipkin](http://zipkin.io/)と統合して、マイクロサービスアーキテクチャに分散トレースを提供できます。Zipkinトレースを有効にするには、`zipkin`のmaven/gradleプロファイルでアプリケーションをパッケージ化し、`spring.zipkin.enabled`プロパティをtrueに設定します。これにより、Zipkinサーバへのスパンレポートがトリガーされ、リクエストヘッダーとログに相関ID（TraceId、SpanId、ParentId）が追加されます。

Zipkinは、マイクロサービス間の依存関係を時間の経過とともに視覚化できるサービス依存性グラフ機能も提供します。

トレース情報をZipkinに報告するようにアプリケーションを設定する方法については、公式の[Spring Cloud Sleuthドキュメント](https://cloud.spring.io/spring-cloud-sleuth/reference/html/#sending-spans-to-zipkin)に従ってください。

[jhipster-metrics-page]: {{ site.url }}/images/jhipster_metrics_page.png "JHipster Metrics page"
[grafana-micrometer-dashboard]: {{ site.url }}/images/monitoring_grafana_micrometer.png "Grafana Micrometer Dashboard" 
