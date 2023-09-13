---
layout: default
title: JHipsterを開発環境で使用する
permalink: /development/
redirect_from:
  - /development.html
sitemap:
    priority: 0.7
    lastmod: 2023-01-05T00:00:00-00:00
---

# <i class="fa fa-code"></i> JHipsterを開発環境で使用する

_**新しいJHipsterアプリケーションの作成については、[ビデオチュートリアル]({{ site.url }}/video-tutorial/)を参照してください！**_

## サマリー

1.  [一般構成](#general-configuration)
2.  [Javaサーバの実行](#running-java-server)
3.  [Angular/Reactでの作業](#working-with-angular)
4.  [データベースを使用する](#using-a-database)
5.  [国際化](#internationalization)

<h2 id="general-configuration">一般構成</h2>

### IDE構成

IDEをまだ設定していない場合は、[IDEの設定]({{ site.url }}/configuring-ide/)ページに移動してください。

### アプリケーション構成

デフォルトでは、JHipsterは「開発」プロファイルを使用するため、何も設定する必要はありません。

利用可能なプロファイルの詳細については、「[プロファイル]({{ site.url }}/profiles/)」というタイトルのセクションを参照してください。

特定のJHipsterプロパティを設定する場合は、[共通アプリケーションプロパティ]({{ site.url }}/common-application-properties/)ページを参照してください。

<h2 id="running-java-server">Javaサーバの実行</h2>

### "main"のJavaクラスとして

IDEで、Javaパッケージ階層のルートにある"Application"クラスを右クリックし、直接実行します。IDEからのデバッグもできます。

このアプリケーションは、[http://localhost:8080](http://localhost:8080)で利用可能です。

このアプリケーションでは「ホットリロード」がデフォルトで有効になっているため、クラスをコンパイルすると、Springアプリケーションのコンテキストが自動的に更新され、サーバーを再起動する必要はありません。

### Mavenプロジェクトとして

Mavenを使用してJavaサーバーを起動できます。JHipsterにはMavenラッパーが用意されているため、Mavenをインストールする必要はありません。また、すべてのプロジェクトユーザーが同じバージョンのMavenを使用できることが保証されます。

`./mvnw`（Mac OS X/Linuxの場合）または `mvnw`（Windowsの場合）

（これにより、デフォルトのMavenタスクである`spring-boot:run`が実行されます）

このアプリケーションは、[http://localhost:8080](http://localhost:8080)で利用可能です。

`npm start`でライブリロードを使用する場合は、次の方法でwebpackタスクを除外することで、サーバの起動を高速化できます。

`./mvnw -P-webapp`

または、Mavenがインストールされている場合は、Mavenを使用してJavaサーバを起動できます。

`mvn`

Mavenの使用方法の詳細については、[http://maven.apache.org](http://maven.apache.org)を参照してください。

### （オプション）Gradleプロジェクトとして

Gradleオプションを選択した場合、JHipsterはGradleラッパーを提供するので、Gradleをインストールする必要はなく、すべてのプロジェクトユーザーが同じGradleバージョンを持っていることが保証されます。

`./gradlew`（Mac OS X/Linuxの場合）または`gradlew`（Windowsの場合）

（これにより、デフォルトのGradleタスクである`bootRun`が実行されます）

このアプリケーションは、[http://localhost:8080](http://localhost:8080)で利用可能です。

`npm start`でライブリロードを使用する場合は、次の方法でwebpackタスクを除外することで、サーバの起動を高速化できます。

`./gradlew -x webapp`

あるいは、Gradleをインストールしている場合は、GradleでJavaサーバを起動できます。

`gradle`

Gradleの使用方法の詳細については、[https://gradle.org](https://gradle.org)を参照してください。

<h2 id="working-with-angular">Angular/Reactの操作</h2>

### Webpackの実行

_このステップは、TypeScriptコードの変更を確認し、クライアントサイドコードのライブリロードを行うために必要です。_

Webpackの実行は`package.json`ファイルのデフォルトタスクなので、実行するにはこれで十分です。

`npm start`

これにより、非常に優れた機能が提供されます。

*   HTML/CSS/TypeScriptファイルのいずれかを変更すると、ブラウザが自動的に更新されます。
*   複数の異なるブラウザまたはデバイスでアプリケーションをテストする場合、すべてのクリック/スクロール/入力が、すべての画面で自動的に同期されることになります。

これにより、以下が起動されます。

- Webpackタスク：TypeScriptコードをJavaScriptに自動的にコンパイルします。
- Webpackの"hot module reload"サーバ：[http://localhost:9060/](http://localhost:9060/)で動作します（バックエンドにアクセスするための[http://127.0.0.1:8080/api](http://127.0.0.1:8080/api)へのプロキシがあります）。
- BrowserSyncタスク：[http://localhost:9000/](http://localhost:9000/)で動作します。[http://localhost:9060/](http://localhost:9060/)（Webpackの"hot module reload"サーバ）へのプロキシを持ち、ユーザのクリック/スクロール/入力を同期します。
- BrowserSync UI：[http://localhost:3001/](http://localhost:3001/)で使用可能です。

**注意:** BrowserSyncはデフォルトで[ghostMode](https://browsersync.io/docs/options#option-ghostMode)を有効にしているため、
特に[複数のブラウザタブを使用する場合](https://github.com/jhipster/generator-jhipster/issues/11116#issuecomment-589362814)において混乱を招く可能性があります。
このghostModeはいつでもオフにできます。ghostModeを簡単に無効にするために、いくつかのコメントコードが`webpack.dev.js`に提供されています。

### NPMの実行

プロジェクトの直接的な依存関係は`package.json`に設定されますが、推移的な依存関係は`npm install`が実行されるときに生成される`package-lock.json`ファイルに定義されます。

プロジェクトのすべてのチームメンバーがすべての依存関係の同じバージョンを持つように、[`package-lock.json`](https://docs.npmjs.com/files/package-lock.json)をソース管理にチェックインすることをお勧めします。`npm install`を再度実行すると、最新バージョンの推移的な依存関係を持つ`package-lock.json`が再生成されます。

### その他のNPMタスク

ここではいくつかの`npm`コマンドの例を示します。

- `npm run lint`: TypeScriptコード内のコードスタイルの問題をチェックします。
- `npm run lint:fix`: TypeScriptのlint問題を自動的に修正します。
- `npm run tsc`: TypeScriptコードをコンパイルします。
- `npm run test`: Jestを使ってユニットテストを実行します。
- `npm run test:watch`: コードが変更されたときのライブフィードバックのために、Jestユニットテストを実行したままにします。
- `npm run e2e`: Protractorを使用して"end to end"テストを実行します（プロジェクトの生成時にProtractorオプションが選択されている場合にのみ機能します）。

<h2 id="using-a-database">データベースの使用</h2>

### データベースの実行

MySQL、MariaDB、PostgreSQL、MSSQL、MongoDB、Cassandra、Couchbaseなどの非組み込みデータベースを使用する場合は、そのデータベースをインストールして設定する必要があります。

JHipsterで最も簡単で推奨される方法は、Docker Composeを使用することです。[Docker Composeガイドはこちらです]({{ site.url }}/docker-compose/)。

データベースを手動でインストールして設定したい場合は、スキーマとそのユーザを作成する必要があります。これは、Liquibaseが既存のスキーマ内のオブジェクト（テーブル、インデックス、等）のみを作成するためです。次に、`src/main/resources/config/application-*.yml`ファイル内のSpring Bootプロパティ（たとえば、データベースURL、ログイン、パスワード）を適宜設定することを忘れないでください。

### 開発中のH2データベースの使用

H2データベースを選択すると、メモリー内のデータベースがアプリケーション内で実行され、デフォルトで[http://localhost:8080/h2-console](http://localhost:8080/h2-console) からコンソールにアクセスできます。

データベースに接続するには、事前設定されたオプションを選択します。

*   Driver Class: org.h2.Driver
*   JDBC URL: jdbc:h2:mem:jhipster
*   User name: <blank>
*   Password: <blank>

![]({{ site.url }}/images/h2.png)

### 開発でのMySQL、MariaDB、またはPostgreSQLの使用

このオプションは、H2を使用するよりも少し複雑ですが、いくつかの重要な利点があります。

*   アプリケーションを再起動してもデータは保持されます。
*   アプリケーションの起動が少し速くなります。
*   優れた`./mvnw liquibase:diff`ゴールを使用できます（以下を参照）。

**注**:MySQLの場合、次のオプションを使用してデータベースを起動する必要があります。

*   `--lower_case_table_names=1`: [MySQLスキーマオブジェクト名のドキュメント](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html)を参照
*   `--skip-ssl`: [MySQLサーバーオプションのドキュメント](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_ssl)を参照
*   `--character_set_server=utf8`: [MySQLサーバシステム変数のドキュメント](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_character_set_server)を参照
*   `--explicit_defaults_for_timestamp` : [MySQLサーバシステム変数のドキュメント](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_explicit_defaults_for_timestamp)を参照

コマンドは以下のとおりです。

    mysqld --lower_case_table_names=1 --skip-ssl --character_set_server=utf8 --explicit_defaults_for_timestamp

## データベースの更新

JPAエンティティを追加または変更する場合は、データベーススキーマを更新する必要があります。

JHipsterは[Liquibase](http://www.liquibase.org)を使用してデータベースの更新を管理し、その設定を`/src/main/resources/config/liquibase/`ディレクトリに保存します。

Liquibaseを使用するには、次の3つの方法があります。
*  エンティティサブジェネレータを使用
*  Liquibaseプラグインを使用
*  設定ファイルを手動で更新

### エンティティサブジェネレータによるデータベースの更新

[エンティティサブジェネレータ]({{ site.url }}/creating-an-entity/)を使用する場合、開発ワークフローは次のようになります。

*   [エンティティサブジェネレータ]({{ site.url }}/creating-an-entity/)を実行します。
*   新しい「変更ログ」が`src/main/resources/config/liquibase/changelog`ディレクトリに作成され、`src/main/resources/config/liquibase/master.xml`ファイルに自動的に追加されます。
*   この変更ログを確認してください。このログは、次にアプリケーションを実行したときに適用されます。

### Liquibaseプラグインによるデータベースの更新

開発でH2、MySQL、MariaDB、またはPostgreSQLを使用することを選択した場合は、このセクションに従って自動的に変更ログを生成できます。

*注:インメモリパーシスタンスでH2を実行している場合は、liquibaseコマンドを実行する前にアプリケーションを起動する必要があります。*

#### Maven

[Liquibase Hibernate](https://github.com/liquibase/liquibase-hibernate)は、`pom.xml`で構成されるMavenプラグインであり、Springの`application.yml`ファイルから独立しています。そのため、デフォルト設定を変更した場合（データベースパスワードを変更した場合など）は、両方のファイルを変更する必要があります。

開発ワークフローは次のとおりです。

1.   JPAエンティティーを変更します（フィールドやリレーションシップの追加など）。
2.   そのエンティティに対して再生成されたliquibaseファイル`config/liquibase/changelog/DATE_added_entity_ENTITY_NAME.xml`の変更をスキップして、次に示す間もなく生成されるchangelogファイルとの競合を回避します。
3.   アプリケーションをコンパイルします（コンパイルされたJavaコードで動作しますので、コンパイルを忘れないようにしてください）。
4.   `./mvnw liquibase:diff`を実行します（または事前にコンパイルするには`./mvnw compile liquibase:diff`を実行します）。
5.   新しい「変更ログ」が`src/main/resources/config/liquibase/changelog`ディレクトリに作成されます。
6.   この変更ログを確認し、次にアプリケーションを実行するときに適用されるように、それを`src/main/resources/config/liquibase/master.xml`ファイルに追加します。

#### Gradle

[Liquibase gradleプラグイン](https://github.com/liquibase/liquibase-gradle-プラグイン)は、`build.gradle`で設定されるGradleプラグインであり、Springの`application.yml`ファイルから独立しています。そのため、デフォルト設定を変更した場合（データベースパスワードを変更した場合など）は、両方のファイルを変更する必要があります。

Mavenと同じワークフローを使用できますが、4番目のステップでは`./gradlew liquibaseDiffChangelog -PrunList=diffLog`を実行する必要があります。

### 変更ログを手動で編集してデータベースを更新

データベースの更新を手動で行いたい（または行う必要がある）場合の開発ワークフローを次に示します。

*   JPAエンティティを変更します（フィールドやリレーションシップの追加など）。
*   `src/main/resources/config/liquibase/changelog`ディレクトリに新しい「変更ログ」を作成します。そのディレクトリ内のファイルには、作成日（yyyyMMddHHmmss形式）の接頭辞を付け、その後、それらの動作を説明するタイトルを付けます。たとえば、`20141006152300_added_price_to_product.xml`は良い名前です。
*   この「変更ログ」ファイルを`src/main/resources/config/liquibase/master.xml`ファイルに追加して、次にアプリケーションを実行したときに適用されるようにします。

Liquibaseの使い方の詳細については、[http://www.liquibase.org](http://www.liquibase.org)にアクセスしてください。

<h2 id="internationalization">国際化</h2>

国際化（またはi18n）はJHipsterの第一級市民であり、プロジェクトの最初に（後付けではなく）設定する必要があると考えています。

使用方法は次のとおりです。

- Angularでは、[NG2 translate](https://github.com/ocombe/ng2-translate)と専用のJHipsterコンポーネントにより、翻訳にJSONファイルを使用して翻訳を実現できます。
- Reactでは、専用のJHipsterコンポーネントにより、Angularコンポーネントと同じように動作し、同じファイルを使用できます。

例えば、"first name"フィールドに翻訳を追加するには、`<label jhiTranslate="settings.form.firstname">First Name</label>`というキーを持つ"translate"属性を追加します。

このキーは、翻訳されたStringを返すJSONドキュメントを参照します。Angular/Reactは、"First Name"の文字列を翻訳されたバージョンに置き換えます。

言語の使用方法の詳細については、[新しい言語のインストールに関するドキュメント]({{ site.url }}/installing-new-languages/)を参照してください。
