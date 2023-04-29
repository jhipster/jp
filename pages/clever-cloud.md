---
layout: default
title: クラウドへのデプロイ
permalink: /clever-cloud/
redirect_from:
  - /clever-cloud.html
sitemap:
    priority: 0.7
    lastmod: 2020-10-09T00:00:00-00:00
---

# Clever Cloudへのデプロイ
[Clever cloud](https://www.clever-cloud.com/){:target="_blank" rel="noopener"}はIT自動化プラットフォームです。

[<img src="{{ site.url }}/images/logo/logo_clever_cloud.png" alt="Clever cloud logo" width="300px" />](https://www.clever-cloud.com/){:target="_blank" rel="noopener"}

## 開始する前に

[Clever cloud CLI](https://www.clever-cloud.com/doc/clever-tools/getting_started/){:target="_blank" rel="noopener"}をインストールする必要があります。

また、[Clever Cloudアカウントを作成](https://api.clever-cloud.com/v2/sessions/signup){:target="_blank" rel="noopener"}し、次のコマンド`clever login`を実行してCLIでログインする必要があります。
<pre>
Opening https://console.clever-cloud.com/cli-oauth?cli_version=2.7.1&cli_token=XXX in your browser to log you in…
Login successful as ...
</pre>


## Clever Cloudアプリケーションを作成する

1. mavenの場合は`clever create --type maven [your application name]`、gradleの場合は`clever create --type gradle [your application name]`となります。

2. データベースアドオンをアプリケーションに追加します。`clever addon create [addon provider] [your addon name] --link [your application name]`

    サポートされているアドオンプロバイダの一覧は`clever addon providers`で出力されます。    
    <pre>
    cellar-addon      Cellar S3 storage       S3-like online file storage web service
    config-provider   Configuration provider  Expose configuration to your applications  (via environment variables)
    es-addon          Elastic Stack           Elasticsearch with Kibana and APM server as options
    fs-bucket         FS Buckets              Persistent file system for your application
    mongodb-addon     MongoDB                 A noSQL document-oriented database
    mysql-addon       MySQL                   An open source relational database management system
    postgresql-addon  PostgreSQL              A powerful, open source object-relational database system
    redis-addon       Redis                   Redis by Clever Cloud is an in-memory key-value data store, powered by Clever Cloud
    </pre>

    [サポートされているアドオンはこちらを参照ください](https://www.clever-cloud.com/doc/addons/clever-cloud-addons/#available-add-ons)

3. 環境変数をセットアップします。`clever env set CC_PRE_RUN_HOOK "cp ./clevercloud/application-clevercloud.yml ./application-prod.yml"`

4. 専用ビルドを有効にします `clever scale --build-flavor M`

    [専用ビルドを参照ください](https://www.clever-cloud.com/doc/admin-console/apps-management/#dedicated-build)


## JHipsterアプリケーションの設定
1. プロジェクトに`clevercloud/`フォルダを追加します。

2. 事前定義されたclever cloud addon環境変数を使用するための`clevercloud/application-clevercloud.yml`を作成します。

    PostgreSQLの場合
    <pre>
    spring:
        datasource:
            type: com.zaxxer.hikari.HikariDataSource        
            url: jdbc:postgresql://${POSTGRESQL_ADDON_HOST}:${POSTGRESQL_ADDON_PORT}/${POSTGRESQL_ADDON_DB}?useUnicode=true&characterEncoding=utf8&useSSL=false
            username: ${POSTGRESQL_ADDON_USER}
            password: ${POSTGRESQL_ADDON_PASSWORD}
            hikari:
                maximumPoolSize: 2
    </pre>

    MySQLの場合
    <pre>
    spring:
        datasource:
            type: com.zaxxer.hikari.HikariDataSource        
            url: jdbc:mysql://${MYSQL_ADDON_HOST}:${MYSQL_ADDON_PORT}/${MYSQL_ADDON_DB}?useUnicode=true&characterEncoding=utf8&useSSL=false
            username: ${MYSQL_ADDON_USER}
            password: ${MYSQL_ADDON_PASSWORD}
            hikari:
                maximumPoolSize: 2
    </pre>

    MongoDBの場合
    <pre>
    spring:
      data:
        mongodb:
          uri: ${MONGODB_ADDON_URI}
          database: ${MONGODB_ADDON_DB}
    </pre>



3. アプリケーションの起動方法を示すゴールフィールドを含むjsonファイルを追加します。

    mavenの場合
    `clevercloud/maven.json`ファイルを作成し、pom.xmlの**artifactId**を使用します。
    
    <pre>
    {
        "build": {
            "type": "maven",
            "goal": "-Pprod package -DskipTests"
        },
        "deploy": {
        "jarName": "./target/[REPLACE BY ARTIFACTID]-0.0.1-SNAPSHOT.jar"
        }
    }
    </pre>

    gradleの場合
    `clevercloud/gradle.json`ファイルを作成し、gradleを使用します。プロパティは**rootProject.name**を使用します。

    <pre>
    {
        "build": {
            "type": "gradle",
            "goal": "-Pprod bootJar -x test"
        },
        "deploy": {
            "jarName": "./build/libs/[REPLACE BY rootProject.name]-0.0.1-SNAPSHOT.jar"
        }
    }
    </pre>

## アプリケーションのデプロイ
### CLIの使用
デプロイ前にコミットする必要があります。

`git commit -m "Clever deploy"`

その後、実行します。

`clever deploy`

### gitlab CIの使用

gitlab CI/CD環境変数に`$CLEVER_TOKEN`と`CLEVER_SECRET`を定義してください。

このステージを`.gitlab-ci.yml`に追加してください。
<pre>
deploy-to-clever-env:
  stage: deploy
  variables:
    APP_NAME: [clever cloud app name]
    APP_ID: [clever cloud app id]
  script:
    - wget https://clever-tools.cellar.services.clever-cloud.com/releases/latest/clever-tools-latest_linux.tar.gz
    - tar xvzf clever-tools-latest_linux.tar.gz
    - ./clever-tools-latest_linux/clever login --token $CLEVER_TOKEN --secret $CLEVER_SECRET
    - ./clever-tools-latest_linux/clever link ${APP_ID}
    - ./clever-tools-latest_linux/clever deploy -a ${APP_NAME}
  environment:
    name: [env name]
    url: https://${APP_NAME}.cleverapps.io
</pre>

## Githubアクションの使用

Githubシークレットに`CLEVER_TOKEN`と`CLEVER_SECRET`を定義します（Settings > Secret）。

このステップを`.github-action.yml`に追加してください。
<pre>
- uses: actions/checkout@v2
- name: Deploy on cc
  env:
    APP_NAME:[clever cloud app name]
    APP_ID: [clever cloud app id]
  run: |
    git fetch --prune --unshallow
    wget https://clever-tools.cellar.services.clever-cloud.com/releases/latest/clever-tools-latest_linux.tar.gz
    tar xvzf clever-tools-latest_linux.tar.gz
    ./clever-tools-latest_linux/clever login --token ${{ secrets.CLEVER_TOKEN }} --secret ${{ secrets.CLEVER_SECRET }}
    ./clever-tools-latest_linux/clever link ${{ env.APP_ID }}
    ./clever-tools-latest_linux/clever deploy -f -a ${{ env.APP_NAME }}
</pre>

## Javaバージョンの変更

Javaバージョン（デフォルトではJava 11）を選択できます。
```
clever env set CC_JAVA_VERSION 12
```

## 詳細情報

*   [Clever Cloudドキュメント](https://www.clever-cloud.com/doc/)
*   [Clever Cloud Java mavenによるデプロイ](https://www.clever-cloud.com/doc/java/java-maven/)
*   [Clever Cloud Java gradleによるデプロイ](https://www.clever-cloud.com/doc/java/java-gradle/)
