---
layout: default
title: プロダクション環境でのJHipsterの使用
permalink: /production/
redirect_from:
  - /production.html
sitemap:
    priority: 0.7
    lastmod: 2021-03-08T12:00:00-00:00
---

# <i class="fa fa-play-circle"></i> プロダクション環境でのJHipsterの使用

JHipsterは、完全にプロダクション環境に対応し、最適化され、セキュリティで保護されたアプリケーションを生成します。このセクションでは、より重要なオプションについて説明します。急いでいる場合は、通常のプロダクションビルドを実行しますが、セキュリティのセクションを読むことを忘れないでください!

1. [プロダクションパッケージのビルド](#build)
2. [プロダクション環境で実行](#run)
3. [パフォーマンスの最適化](#performance)
4. [セキュリティ](#security)
5. [モニタリング](#monitoring)

<h2 id="build">プロダクションパッケージのビルド</h2>

### プロダクションビルドのテスト

これにより、実際のパッケージを構築することなく、Mavenからのプロダクションビルドをテストできます。

JHipsterを「プロダクション」モードで使用するには、事前に設定された`prod`プロファイルを使用します。Mavenでは、次を実行してください。

`./mvnw -Pprod`

Gradleを使用する場合は、次のコマンドを実行してください。

`./gradlew -Pprod`

このプロファイルは、すべてのプロダクション設定でアプリケーションをコンパイル、テスト、およびパッケージ化します。

使用可能なプロファイルの詳細については、「[開発/プロダクションプロファイル]({{ site.url }}/profiles/)」というタイトルのセクションを参照してください。

### 実行可能なJAR/WARファイルの構築

#### Mavenを使用

- アプリケーションを「プロダクション」JARとしてパッケージ化するには、次のように入力してください。

    `./mvnw -Pprod clean verify`

    これにより、ファイル`target/jhipster-0.0.1-SNAPSHOT.jar`が生成されます（アプリケーションが"jhipster"という名前の場合）。


- アプリケーションを「プロダクション」WARとしてパッケージ化するには、次の手順を実行します。

    - 次のように`pom.xml`を変更して、アプリケーションのパッケージを`war`に変更します。

    ```diff
    -    <packaging>jar</packaging>
    +    <packaging>war</packaging>
    ``` 
    
    - `pom.xml`を変更して、`spring-boot-starter-undertow`依存関係のスコープを`provided`に変更します。

    ```diff
        <id>prod</id>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-undertow</artifactId>
    +           <scope>provided</scope>
            </dependency>
        </dependencies>
    ``` 
    - 元の`war`に沿って実行可能ファイル`war`を生成するには、次のコマンドを入力します。 
    
    ```bash
    ./mvnw -Pprod clean verify
    ```
  - これにより、次のファイルが生成されます（アプリケーションが"jhipster"と言う名前の場合）。
   
    * `target/jhipster-0.0.1-SNAPSHOT.war`
    * `target/jhipster-0.0.1-SNAPSHOT.war.original` 

<<<<<<< HEAD
**注意** コンテキストパスでJARまたはWARファイルを構築し、**かつ**、**Reactクライアント**または**Vueクライアント**を選択した場合、`webpack.prod.js`または`webpack.common.js`（**Vue**の場合は両方のファイル）を適切な`base`属性値で更新する必要があります。
`jhipster`をコンテキストパスとして考えると、`base`属性値は次のようになります。

```
new HtmlWebpackPlugin({
    ...
    base: '/jhipster/'
})
```

**Angularクライアント**を選択した場合は、`index.html`を適切な`base`タグで更新する必要があります。
`jhipster`をコンテキストパスとして考えると、`base`タグの値は次のようになります。

```
<base href="/jhipster/"/>
```

**注意**`prod`プロファイルでJARまたはWARファイルを構築する場合、生成されるアーカイブには`dev`アセットは含まれません。
=======
**Please note** that when building a JAR or WAR file with the `prod` profile, the generated archive will not include the `dev` assets.
>>>>>>> upstream/main


#### Gradleを使用
アプリケーションを「プロダクション」JARとしてパッケージ化するには、次のように入力します。

`./gradlew -Pprod clean bootJar`

これにより、ファイル`build/libs/jhipster-0.0.1-SNAPSHOT.jar`が生成されます（アプリケーションが"jhipster"という名前の場合）。


アプリケーションを「プロダクション」WARとしてパッケージ化するには、次のように入力します。

`./gradlew -Pprod -Pwar clean bootWar`

<<<<<<< HEAD
**注意** コンテキストパスでJARまたはWARファイルを構築し、**かつ**、**Reactクライアント**または**Vueクライアント**を選択した場合、`webpack.prod.js`または`webpack.common.js`（**Vue**の場合は両方のファイル）を適切な`base`属性値で更新する必要があります。
`jhipster`をコンテキストパスとして考えると、`base`属性値は次のようになります。

```
new HtmlWebpackPlugin({
    ...
    base: '/jhipster/'
})
```

**Angularクライアント**を選択した場合は、`index.html`を適切な`base`タグで更新する必要があります。
`jhipster`をコンテキストパスとして考えると、`base`タグの値は次のようになります。

```
<base href="/jhipster/"/>
```

**注意**`prod`プロファイルでJARまたはWARファイルを構築する場合、生成されるアーカイブには`dev`アセットは含まれません。

<h2 id="run">プロダクション環境での実行</h2>
=======
>>>>>>> upstream/main

### アプリケーションサーバーを使用しないJARファイルの実行

多くの人は、アプリケーション・サーバーにデプロイする代わりに、単一の実行可能なJARファイルを持つ方が簡単だと考えています。

前の手順で生成したJARファイルを「プロダクション」モードで実行するには、次のように入力します（Mac OS XまたはLinuxの場合）。

`./jhipster-0.0.1-SNAPSHOT.jar`

Windowsの場合は、次のコマンドを使用します。

`java -jar jhipster-0.0.1-SNAPSHOT.jar`

**注意**このJARファイルは、ビルド時に選択したプロファイルを使用します。前のセクションで`prod`ファイルを使用してビルドされたため、`prod`プロファイルで実行されます。

<<<<<<< HEAD
コンテキストパスは、次のように環境変数またはコマンドラインパラメータとして指定できます。
```bash 
java -jar jhipster.jar --server.servlet.context-path=/jhipster
```

### Dockerコンテナでのアプリケーションの実行
=======
### Running the application in a Docker container
>>>>>>> upstream/main

JHipsterは、Dockerに対する第一級のサポートを提供しています。実行可能なJARファイルをDockerイメージにバンドルして、Docker内で実行します。

Dockerを使ってアプリケーションをパッケージ化する方法については、[Docker Composeドキュメント]({{ site.url }}/docker-compose/)を参照してください。

### サービスとして実行

JarをLinuxサービスとして実行もできます。パッケージ化する前に`pom.xml`ファイルで強制できます。そのためには、`spring-boot-maven-plugin`プラグインの`<configuration>`内に次のプロパティを追加します。

```
<embeddedLaunchScriptProperties>
    <mode>service</mode>
</embeddedLaunchScriptProperties>
```

次に、init.dを以下のように設定します。

`ln -s jhipster-0.0.1-SNAPSHOT.jar /etc/init.d/jhipster`

次の方法でアプリケーションを保護します。

`chown jhuser:jhuser jhipster-0.0.1-SNAPSHOT.jar
sudo chattr +i your-app.jar`

`jhuser`がアプリケーションを実行するrootではないOSアカウントであるとすると、アプリケーションは次のように実行できます。

`service jhipster start|stop|restart`

[Spring Bootドキュメント](https://docs.spring.io/spring-boot/docs/current/reference/html/deployment-install.html)には他にも多くのオプションがあり、より多くのセキュリティ手順やWindowsサービスが含まれています。

<h2 id="performance">パフォーマンスの最適化</h2>

### キャッシュのチューニング

アプリケーションの生成時にキャッシュプロバイダを選択した場合は、JHipsterによって自動的に設定されています。

ただし、デフォルトのキャッシュ値は、スペックが低めのハードウェアでもアプリケーションが実行できるように、かなり低い値になっています。これらの値は、アプリケーション固有のビジネス要件に応じて調整する必要があります。

以下をお読みください。

- [JHipsterの「キャッシュの使用」のドキュメント]({{ site.url }}/using-cache/)では、選択したキャッシュ・プロバイダとそのチューニング方法の詳細を確認できます。
- [モニタリングに関する最後のセクション](#monitoring)では、アプリケーションの実際の使用状況に応じてキャッシュを調整できます。

### HTTP/2のサポート

JHipsterは、`application-prod.yml`ファイルで設定されている`jhipster.http.version`プロパティを使用してHTTP/2をサポートします。

HTTP/2を有効にするには、次の手順を実行する必要があります。

- `jhipster.http.version: V_2_0`を設定します。
- ブラウザがHTTP/2でHTTPSを使用するように強制するため、HTTPSを設定します（このドキュメントの[セキュリティセクション](#security)を参照）。

### GZip圧縮

`prod`プロファイルを使用する実行可能なJARファイル内で、JHipsterはWebリソースにGZip圧縮を設定します。

デフォルトでは、圧縮はすべての静的リソース（HTML、CSS、JavaScript）およびすべてのRESTリクエストに対して機能します。この設定の詳細については、`application-prod.yml`ファイルで設定されているSpring Bootアプリケーションプロパティの`server.compression.*`キーを参照してください。

**注意** GZip圧縮はアプリケーション・サーバーによって行われるため、このセクションは前述の「実行可能JAR」オプションを使用する場合にのみ適用されます。外部アプリケーション・サーバーでアプリケーションを実行する場合は、アプリケーションを個別に構成する必要があります。

### キャッシュ・ヘッダー

`prod`プロファイルを使用して、JHipsterは、静的リソース（JavaScript、CSS、フォントなど）に特定のHTTPキャッシュヘッダーを配置するサーブレットフィルタを設定し、それらがブラウザとプロキシによってキャッシュされるようにします。

### Webpackを使用した最適化されたJavaScriptアプリケーションの生成

このステップは、`prod`プロファイルを使用してプロジェクトを構築するときに自動的にトリガーされます。Mavenビルドを起動せずに実行する場合は、次のコマンドを実行してください。

`npm run build`

これは、[Webpack](https://webpack.github.io/)を使用してすべての静的リソース（CSS, TypeScript, HTML, JavaScript, 画像など）を処理し、最適化されたクライアント側アプリケーションを生成します。

このプロセスの間、WebpackはTypeScriptコードをJavaScriptコードにコンパイルし、ソースマップも生成するため、クライアントサイドアプリケーションをデバッグできます。

これらの最適化されたアセットは、Mavenの場合は`target/classes/static`で、Gradleの場合は`build/resources/main/static`で生成され、最終的なプロダクションJARに含まれます。

このコードは、`prod`プロファイルでアプリケーションを実行するときに提供されます。

<h2 id="security">セキュリティ</h2>

### デフォルトのユーザーおよび管理者アカウントの保護

JHipsterには、いくつかのデフォルト・ユーザーが生成されています。本番環境では、これらのデフォルト・パスワードを変更する必要があります。

これらのパスワードを変更し、アプリケーションをセキュリティで保護する方法については、[セキュリティドキュメント]({{ site.url }}/security/)に従ってください。

### HTTPSサポート

HTTPSは、JHipsterアプリケーションで直接設定することも、特定のフロントエンドプロキシを使用して設定することもできます。

#### JHipsterでのHTTPS設定

HTTPSは、`application-prod.yml`ファイル内のSpring Securityの標準の`server.ssl`設定キーを使用して設定されます。

SSLを有効にするには、次のコマンドを使用して証明書を生成します。

    keytool -genkey -alias <your-application> -storetype PKCS12 -keyalg RSA -keysize 2048 -keystore keystore.p12 -validity 3650

また、[このチュートリアル](https://community.letsencrypt.org/t/tutorial-java-keystores-jks-with-lets-encrypt/34754)によるLet's Encryptの使用もできます。

次に、`application-prod.yml`の設定が次のようになるように、`server.ssl`プロパティを変更します。

    server:
        port: 443
        ssl:
            key-store: keystore.p12
            key-store-password: <your-password>
            keyStoreType: PKCS12
            keyAlias: <your-application>
            ciphers: TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384, TLS_DHE_RSA_WITH_AES_128_GCM_SHA256, TLS_DHE_RSA_WITH_AES_256_GCM_SHA384, TLS_DHE_RSA_WITH_AES_128_CBC_SHA, TLS_DHE_RSA_WITH_AES_256_CBC_SHA, TLS_DHE_RSA_WITH_AES_128_CBC_SHA256, TLS_DHE_RSA_WITH_AES_256_CBC_SHA256
            enabled-protocols: TLSv1.2

暗号スイートは、いくつかの古くて非推奨のSSL暗号を無効にすることによってセキュリティを強化します。このリストは、[SSL Labs](https://www.ssllabs.com/ssltest/)にあります。

`server.ssl.ciphers`プロパティが有効になると、JHipsterはこのプロパティ`jhipster.http.useUndertowUserCipherSuitesOrder`（デフォルトではtrue）を使用してUndertowでの順序を強制します。

`enabled-protocols`は、古いSSLプロトコルを無効にします。

次に、前方秘匿性を実現するための最後の仕上げを行います。JVM起動時に次のフラグを追加します。

    -Djdk.tls.ephemeralDHKeySize=2048

設定をテストするには、[SSL Labs](https://www.ssllabs.com/ssltest/)にアクセスしてください。

全てOKならA+が取得できます。

#### フロントエンドプロキシを使用したHTTPS設定

JHipsterアプリケーションの前にフロントエンドHTTPSプロキシを設定するためのソリューションは数多くあります。

最も一般的な解決策の1つは、Apache HTTPサーバを使用することです。Let's Encryptを使用して設定できます。

- ApacheとLet's Encryptインストール：`apt-get install-y apache2 python-certbot-apache`
- Let's Encryptの設定：`certbot --apache -d <your-domain.com> --agree-tos -m <your-email> --redirect`
- SSL証明書の自動更新を設定：crontablに`10 3 * * * /usr/bin/certbot renew --quiet`を追加

<<<<<<< HEAD
<h2 id="monitoring">モニタリング</h2>
=======
### Custom Context Path

You can specify a context path for your Spring Boot backend by passing in a `server.servlet.context-path` parameter and value:

```bash
java -jar jhipster.jar --server.servlet.context-path=/jhipster/
```

Or, you can add this configuration to `application.yml`:

```
---
server:
  servlet:
    context-path: /jhipster/
```

For frontend bundlers, the context path is a build-time configuration.

**Angular** frontends can be configured using:
- `angular.json`: `projects -> * your project name -> architect -> build -> options -> baseHref : '/jhipster/'`
- `ng build --base-href '/jhipster/'`
- Use [APP_BASE_HREF](https://angular.io/api/common/APP_BASE_HREF)

For **Webpack-based** frontends, you can configure using:

- Webpack configuration file:
```
new HtmlWebpackPlugin({
    ...
    base: '/jhipster/'
})
```

Others modifications may be necessary, like configuring your development server and adjusting iframes in pages like swagger-ui.

**Please note** that using a relative base path like `./` is possible, but you must adjust other configurations to be compatible with it.

<h2 id="monitoring">Monitoring</h2>
>>>>>>> upstream/main

JHipsterは、[Micrometer](https://micrometer.io/)による完全なモニタリングサポートを備えています。

開発環境では、MetricsデータはJMX経由で利用可能であり、JConsoleを起動するとアクセスできます。

プロダクション環境では、アプリケーションがエンドポイント上のメトリックデータを公開することで、[Prometheusサーバ](https://prometheus.io/docs/introduction/overview/)が、設定に応じて定期的にスクレイピングできます。
