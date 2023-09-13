---
layout: default
title: セキュリティ
permalink: /security/
redirect_from:
  - /security.html
sitemap:
    priority: 0.7
    lastmod: 2018-03-18T18:20:00-00:00
---

# <i class="fa fa-lock"></i> アプリケーションをセキュアに

JHipsterによって生成されたもののように、単一のWebページアプリケーションでSpring Securityを使用するには、Ajaxによるログイン/ログアウト/エラービューが必要です。これらのビューを正しく使用するためにSpring Securityを設定し、すべてのJavaScriptとHTMLコードを生成します。

デフォルトでは、JHipsterには2つの異なるユーザがいます。

* "user"：これは"ROLE_USER"権限を持つ通常のユーザーです。デフォルトのパスワードは"user"です。
* "admin"："ROLE_USER"および"ROLE_ADMIN"権限を持つ管理ユーザーです。デフォルトのパスワードは"admin"です。

"ROLE_USER"と"ROLE_ADMIN"の2つの権限は、エンティティに対して同じアクセスを提供します。つまり、"user"は"admin"と同じCRUD操作する権限を与えられています。この動作は、"user"が任意のエンティティを削除できるなどの理由で、アプリケーションが本番に移行するときに問題になる可能性があります。アクセス制御を改善する方法の詳細については、この[ブログ投稿](https://blog.ippon.tech/improving-the-access-control-of-a-jhipster-application/)を参照してください。

セキュリティ上の理由から、運用環境ではこれらのデフォルトパスワードを変更する必要があります。

JHipsterは、3つの主要なセキュリティメカニズムを提供します。

1. [JSON Web Tokens (JWT)](#jwt)
2. [セッションベースの認証](#session)
3. [OAuth 2.0とOpenID Connect](#oauth2)

<h2 id="jwt">JSON Web Tokens (JWT)</h2>

[JSON Web Token (JWT)](https://jwt.io/)認証はステートレス・セキュリティー・メカニズムなので、複数の異なるサーバー上でアプリケーションを拡張したい場合には良い選択肢です。

[マイクロサービスアーキテクチャ](/microservices-architecture/)を使用する場合、これがデフォルトのオプションであることに注意してください。

この認証メカニズムは、デフォルトではSpring Securityには存在せず、[Java JWTプロジェクト](https://github.com/jwtk/jjwt)を統合しJHipsterに特化させたものです。

このソリューションでは、ユーザーのログイン名と権限を保持するセキュア・トークンを使用します。トークンは署名されているため、ユーザーによる変更はできません。

JHipsterは、無効なJWTをカスタムアプリケーションメトリクスとして自動的に追跡します。[モニタリングドキュメント](/monitoring/#security-metrics)を参照してください。

### JWTをセキュアに

- JHipsterは、`jhipster.security.authentication.jwt.secret`と`jhipster.security.authentication.jwt.base64-secret`という2つのSpring Bootプロパティを使用して設定できる秘密鍵を使用します。
2番目のオプションは、Base 64でエンコードされた文字列を使用し、より安全であると考えられるため、推奨します。両方のプロパティが設定されている場合は、レガシーな理由により、`secret`プロパティ（セキュリティが低い方）が使用されます。
Base64プロパティを使用しない場合は、アプリケーションの起動時に警告が表示されます。
- これらのキーの最小長は512ビットである必要があります。十分な長さがない場合は、ログインに使用できません。その場合は、コンソールにその問題を説明する明確な警告が表示されます。
- 秘密鍵は`application-*.yml`ファイルで設定されています。これらの鍵は秘密にしておく必要があるので、プロダクションのプロファイル用に安全な方法で保管する**必要があります**。
通常、Spring Bootプロパティ設定を使用して設定できます。[JHipster Registry](/jhipster-registry/)のようなSpring Cloud Configサーバを使用するか、
環境変数を使用するか、システム管理者によってアプリケーションの実行可能なWARファイルと同じディレクトリにSCPで置かれた特有の`application-prod.yml`ファイルを使用します。
- デフォルトの"user"および"admin"パスワードは**変更する必要があります**。これを行う最も簡単な方法は、アプリケーションをデプロイし、"user/user"としてログインしてから"admin/admin"としてログインし、それぞれに対して"Account > Password"メニューを使用してパスワードを変更することです。

<h2 id="session">セッションベースの認証</h2>

これは「古典的な」Spring Security認証メカニズムですが、大幅に改善されています。HTTPセッションを使用するため、ステートフルなメカニズムです。複数のサーバでアプリケーションを拡張する場合は、各ユーザが同じサーバにとどまるように、スティッキセッションを備えたロードバランサを使用するか、[Spring Session](https://spring.io/projects/spring-session)を追加して、メモリではなくデータベースにセッションを格納することを検討する必要があります。

### セッションベースの認証をセキュアに

- Remember-me認証の場合、Remember-meキーは`application-dev.yml`および`application-prod.yml`ファイル内で、`jhipster.security.remember-me.key`プロパティとして設定されます。このキーは秘密にしておく必要があるため、プロダクションのプロファイル用に安全な方法で保存する**必要があります**。通常、Spring Bootプロパティ設定を使用して設定できます。[JHipster Registry](/jhipster-registry/)のようなSpring Cloud Configサーバを使用するか、環境変数を使用するか、システム管理者によってアプリケーションの実行可能なWARファイルと同じディレクトリにSCPで置かれた特有の`application-prod.yml`ファイルを使用します。
- デフォルトの"user"および"admin"パスワードは**変更する必要があります**。これを行う最も簡単な方法は、アプリケーションをデプロイし、"user/user"としてログインしてから"admin/admin"としてログインし、それぞれに対して"Account > Password"メニューを使用してパスワードを変更することです。

### remember-meメカニズムの改善

私たちは、Spring Securityのremember-meメカニズムを変更して、データベース（SQLまたはNoSQLデータベースなど生成時の選択に応じて！）に格納される独自のトークンを持つようにしました。また、標準の実装よりも多くの情報を格納するようにし、トークンの出所（IPアドレス、ブラウザ、日付など）をよりよく理解できます。さらに、完全な管理画面を生成し、別のコンピュータでログアウトするのを忘れた場合などにセッションを無効にできるようにしました。

### Cookieの盗難対策

私たちは、完成度の高いCoockie盗難防止メカニズムを追加しました。あなたのセキュリティ情報をCookieとデータベースに保存し、ユーザーがログインするたびにそれらの値を修正し、それらが変更されたかどうかをチェックします。そうすることで、誰かがあなたのCoockieを盗んだ場合でも、使用できるのは最大で1回だけます。

<h2 id="oauth2">OAuth 2.0とOpenID Connect</h2>

OAuthは、HTTPセッションのようなステートフルなセキュリティメカニズムです。Spring Securityは、優れたOAuth 2.0とOIDCのサポートを提供しており、これはJHipsterによって活用されています。OAuthとOpenID Connect(OIDC)が何であるかわからない場合は、[OAuthとは何か?](https://developer.okta.com/blog/2017/06/21/what-the-heck-is-oauth)を参照してください。

### Keycloak

[Keycloak](https://www.keycloak.org)は、JHipsterで設定されたデフォルトのOpenID Connectサーバです。

アプリケーションにログインするには、[Keycloak](https://www.keycloak.org)を起動して実行する必要があります。JHipsterチームは、デフォルトのユーザーとロールを持つDockerコンテナを作成しました。次のコマンドを使用してKeycloakを起動します。

```shell
docker-compose -f src/main/docker/keycloak.yml up
```
あるいは、次のような`npm`の使用もできます。

```shell
npm run docker:keycloak:up
```

Docker ComposeでKeycloakを使用したい場合は、[Docker Composeドキュメント](/docker-compose/)を必ず読み、Keycloak用に`/etc/hosts`を正しく設定してください。

> <i class="fa fa-info-circle"></i>**Apple Silicon(M1)上のJHipster 7.8.1およびKeycloak 16.1.0に関する注意**
> 
> v18より前のKeycloakは、互換モードのApple Siliconで誤動作する可能性があり、解決策は明らかではありません。この問題はKeycloakイメージをローカルに構築することで解決できます。
> 
> ```
> git clone git@github.com:keycloak/keycloak-containers.git
> cd keycloak-containers/server
> git checkout 16.1.0
> docker build -t jboss/keycloak:16.1.0 .
> ```

Docker ComposeでKeycloakを使用したい場合は、[Docker Composeドキュメント](/docker-compose/)を必ず読み、Keycloak用に`/etc/hosts`を正しく設定してください。（訳注：上述の文章と重複してますが原文そのままにしています）

このイメージには、`src/main/resources/config/application.yml`のセキュリティ設定が構成されています。上記の`/etc/hosts`に関する注意を参照し、`issuer-uri`を変更する必要がある場合があることに注意してください。

```yaml
spring:
  ...
  security:
    oauth2:
      client:
        provider:
          oidc:
            issuer-uri: http://localhost:9080/auth/realms/jhipster
            # localhostは、ホストではなく、ゲスト(コンテナ)にバインドされます。
            # Keycloakをデーモンとして実行するには、npm run docker:keycloak:upとなり、/etc/hostsの編集と、
            # issuer-uriを次のようにする必要があります。
            # issuer-uri: http://keycloak:9080/auth/realms/jhipster
        registration:
          oidc:
            client-id: web_app
            client-secret: web_app
            scope: openid,profile,email
```

Keycloakはデフォルトで組み込みH2データベースを使用しているため、Dockerコンテナを再起動すると、作成されたユーザが失われます。データを保持するには、[Keycloak Dockerドキュメント](https://hub.docker.com/r/jboss/keycloak/)を参照してください。H2データベースを保持する1つの解決策は、以下を実施します。

- 永続化するボリュームを追加します：`./keycloak-db:/opt/jboss/keycloak/standalone/data`
- マイグレーション方法を`OVERWRITE_EXISTING`から`IGNORE_EXISTING`に変更します（コマンドセクション内）

本番環境では、HTTPSを使用することがKeycloakによって要求されます。これを実現するには、HTTPSを管理するリバース・プロキシまたはロード・バランサを使用するなど、いくつかの方法があります。このトピックの詳細を知るには、[Keycloak HTTPSドキュメント](https://www.keycloak.org/docs/latest/server_installation/index.html#setting-up-https-ssl)を読むことをお薦めします。

### Okta

Keycloakの代わりにOktaを使用したい場合は、[Okta CLI](https://cli.okta.com/)を使用するとかなり早いです。インストールしたら、次のコマンドを実行します。

```shell
okta register
```

次に、JHipsterアプリのディレクトリで`okta apps create jhipster`を実行します。これにより、Oktaアプリが設定され、`ROLE_ADMIN`グループと`ROLE_USER`グループが作成され、Okta設定を含む`.okta.env`ファイルが作成され、IDトークンに`groups`クレームが設定されます。

`source .okta.env`を実行し、MavenまたはGradleでアプリを起動します。登録した資格情報を使用してサインインできるはずです。

Windowsの場合は、`source`コマンドが動作するように、[WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)をインストールする必要があります。

Okta Admin Consoleから手動で設定する場合は、次の手順を参照してください。

#### Okta管理コンソールを使用したOIDCアプリケーションの作成

まず、<https://developer.okta.com/signup>で無料の開発者アカウントを作成する必要があります。その後、`https://dev-123456.okta.com`のような名前の独自のOktaドメインを取得します。

Oktaの設定を使うために`src/main/resources/config/application.yml`を変更します。ヒント：`{yourOktaDomain}`をあなたの組織の名前に置き換えてください（例：`dev-123456.okta.com`）。

```yaml
security:
  oauth2:
    client:
      provider:
        oidc:
          issuer-uri: https://{yourOktaDomain}/oauth2/default
      registration:
        oidc:
          client-id: {client-id}
          client-secret: {client-secret}
          scope: openid,profile,email
```

OktaでOIDCアプリを作成し、`{client-id}`と`{client-secret}`を取得します。これを行うには、Okta Developerアカウントにログインし、**Applications** > **Applications** > **Add Application** > **Create New App**に移動します。**Web**, **OpenID Connect**を選択し、**Create**をクリックします。アプリに覚えやすい名前を付け、ログインリダイレクトURIとして`http://localhost:8080/login/oauth2/code/oidc`を指定します。ログアウトリダイレクトURIとして`http://localhost:8080`を追加し、**Save**をクリックします。クライアントIDとシークレットを`application.yml`ファイルにコピーします。

`ROLE_ADMIN`および`ROLE_USER`グループを作成し（**Directory** > **Groups** > **Add Group**）、それらにユーザーを追加します。サインアップしたアカウントを使用するか、新しいユーザーを作成します（**Directory** > **People** > **Add Person**）。**Security** > **API** > **Authorization Servers**に移動し、`default`サーバーをクリックします。**Claims**タブをクリックし、**Add Claim**をクリックします。`groups`という名前を付けて、IDトークンに含めます。値のタイプを`Groups`に設定し、フィルタを`.*`の正規表現に設定します。**Create**をクリックします。

<img src="/images/security-add-claim.png" alt="Add Claim" width="600" style="margin: 10px"> 

これらを変更した後、問題なく使用できるはずです！　もし問題があれば[Stack Overflow](https://stackoverflow.com/questions/tagged/jhipster)に投稿してください。質問には必ず"jhipster"と"okta"のタグを付けてください。

e2eテストの実行時にOktaを使用するには、環境変数を設定できます。

```shell
export CYPRESS_E2E_USERNAME=<your-username>
export CYPRESS_E2E_PASSWORD=<your-password>
```

Protractorを使用している場合は、`CYPRESS_`プレフィックスを削除してください。

#### 環境変数の使用

環境変数を使用してデフォルトの上書もできます。次に例を示します。

```bash
export SPRING_SECURITY_OAUTH2_CLIENT_PROVIDER_OIDC_ISSUER_URI="https://{yourOktaDomain}/oauth2/default"
export SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_OIDC_CLIENT_ID="{client-id}"
export SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_OIDC_CLIENT_SECRET="{client-secret}"
```

これを`~/.okta.env`ファイルに入れて`source ~/.okta.env`を実行すると、KeycloakをOktaでオーバーライドできます。

次に、Herokuにデプロイするときにこれらのプロパティを設定できます。

```bash
heroku config:set \
  SPRING_SECURITY_OAUTH2_CLIENT_PROVIDER_OIDC_ISSUER_URI="$SPRING_SECURITY_OAUTH2_CLIENT_PROVIDER_OIDC_ISSUER_URI" \
  SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_OIDC_CLIENT_ID="$SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_OIDC_CLIENT_ID" \
  SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_OIDC_CLIENT_SECRET="$SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_OIDC_CLIENT_SECRET"
```

<a name="create-native-app-okta"></a>
#### Oktaでモバイル用のネイティブアプリを作成する

JHipsterの[Ionic](https://github.com/jhipster/generator-jhipster-ionic)または[React Native](https://github.com/jhipster/generator-jhipster-react-native)のBlueprintを使用してモバイルアプリを開発している場合、OIDCを使用しているなら、Oktaでネイティブアプリを作成することになる可能性があります。

[Okta CLI](https://cli.okta.com)を使用して`okta apps create`を実行します。デフォルトのアプリ名を選択するか、必要に応じて変更します。**Native**を選択して**Enter**を押します。

- **Ionic**：リダイレクトURIを`[http://localhost:8100/callback,dev.localhost.ionic:/callback]`に変更し、ログアウトリダイレクトURIを`[http://localhost:8100/logout,dev.localhost.ionic:/logout]`に変更します。
- **React Native**：リダイレクトURIには`[http://localhost:19006/,https://auth.expo.io/@<username>/<appname>]`を使用してください。

**注意:** `dev.localhost.ionic`はデフォルトのスキームですが、`com.okta.dev-133337`（ここで`dev-133337.okta.com`はあなたのOkta OrgのURLです）のような、よりトラディショナルなものも使用できます。これを変更する場合は、Ionicアプリの`src/environments/environment.ts`の`scheme`を必ず更新してください。

Okta CLIは、Okta OrgにOIDC Appを作成します。指定したリダイレクトURIを追加し、Everyoneグループへのアクセスを許可します。

```shell
Okta application configuration:
Issuer:    https://dev-133337.okta.com/oauth2/default
Client ID: 0oab8eb55Kb9jdMIr5d6
```

**注意**：Okta管理コンソールを使用してもアプリを作成できます。詳細については、[ネイティブアプリの作成](https://developer.okta.com/docs/guides/sign-into-mobile-app/create-okta-application/)を参照してください。

#### Ionicアプリをアップデートする

`ionic/src/environments/environment.ts`を開き、NativeアプリからクライアントIDを追加します。`server_host`の値はJHipsterアプリ（`/api/auth-info`）から検索されますが、フォールバック（代替）値として定義できます。以下は例です。

```ts
oidcConfig: {
  client_id: '<native-client-id>',
  server_host: 'https://<your-okta-domain>/oauth2/default',
  ...
}
```

また、`http://localhost:8100`用にトラステッド・オリジンを追加する必要があります。Okta Admin Consoleで、**Security** > **API** > **Trusted Origins** > **Add Origin**に移動します。次の値を使用します。

- Name: `http://localhost:8100`
- Origin URL: `http://localhost:8100`
- Type: CORS and Redirectの**両方を**チェック

**Save**をクリックします。

Ionicアプリを再起動して、Oktaでログインします!

#### Reactネイティブアプリのアップデート

クライアントIDを`app/config/app-config.js`にコピーします。

Ionicアプリを再起動して、Oktaでログインします!

#### OpenID Connectチュートリアル

JHipster 5とOIDC with Oktaの詳細については、[JHipsterでOpenID Connectサポートを使用する](https://developer.okta.com/blog/2017/10/20/oidc-with-jhipster)を参照してください。

JHipster 6を使用している場合は、[Java 12とJHipster 6によるJavaの改善、高速化、軽量化](https://developer.okta.com/blog/2019/04/04/java-11-java-12-jhipster-oidc)を参照してください。JHipster 6でマイクロサービスを使用している場合は、[Spring Cloud ConfigとJHipsterを使ったJavaマイクロサービス](https://developer.okta.com/blog/2019/05/23/java-microservices-spring-cloud-config)を参照してください。

JHipster 7については、[Spring BootとJHipsterを使ったリアクティブJavaマイクロサービス](https://developer.okta.com/blog/2021/01/20/reactive-java-microservices)を参照してください。

Okta開発者ブログには、MicronautとQuarkusへの ❤️ も掲載されています。

- [JHipsterでセキュアなMicronautとAngularアプリを構築する](https://developer.okta.com/blog/2020/08/17/micronaut-jhipster-heroku)
- [QuarkusとJHipsterで高速Java簡単に](https://developer.okta.com/blog/2021/03/08/jhipster-quarkus-oidc)

### Auth0

Keycloakの代わりに[Auth0](https://auth0.com/)を使用する場合は、次の設定手順に従います。

#### Auth0 Admin Dashboardを使用したOIDCアプリケーションの作成

- <https://auth0.com/signup>で無料の開発者アカウントを作成します。サインアップが成功すると、アカウントは`dev-xxx.us.auth0.com`のような独自のドメインに関連付けられます。
- `Regular Web Applications`タイプの新しいアプリケーションを作成します。`Settings` タブに切り替えて、次のようにアプリケーションの設定を構成します。
    - Allowed Callback URLs: `http://localhost:8080/login/oauth2/code/oidc`
    - Allowed Logout URLs: `http://localhost:8080/`
    - 注意：Consulを使用している場合は、ポート8500のURLも追加します。
    - 注意：JHipsterレジストリを使用している場合は、ポート8761のURLも追加します。
- **User Management** > **Roles**に移動し、`ROLE_ADMIN`および`ROLE_USER`という名前の新しいロールを作成します。
- **User Management** > **Users**に移動し、新しいユーザーアカウントを作成します。 **Role**タブをクリックして、新しく作成したユーザーアカウントに役割を割り当てます。
- **Actions** > **Flows**に移動し、**Login**を選択します。`Add Roles`という名前の新しいアクションを作成し、デフォルトのトリガーとランタイムを使用します。`onExecutePostLogin`ハンドラを次のように変更します。

  ```js
  exports.onExecutePostLogin = async (event, api) => {
    const namespace = 'https://www.jhipster.tech';
    if (event.authorization) {
      api.idToken.setCustomClaim('preferred_username', event.user.email);
      api.idToken.setCustomClaim(`${namespace}/roles`, event.authorization.roles);
      api.accessToken.setCustomClaim(`${namespace}/roles`, event.authorization.roles);
    }
  }
  ```
- **Deploy**を選択し、`Add Roles`アクションをログインフローにドラッグします。

_これらの手順をすべて自動化したい場合は、Auth0 CLIプロジェクトの[issue #351](https://github.com/auth0/auth0-cli/issues/351)に👍を追加してください。_

#### Auth0をOIDCプロバイダとして使用するようにJHipsterアプリケーションを構成

`JHipster`アプリケーションで、Auth0設定を使用するように`src/main/resources/config/application.yml`を変更します。

```yaml
spring:
  ...
  security:
    oauth2:
      client:
        provider:
          oidc:
            # 必ず最後のスラッシュを含めるようにしてください！
            issuer-uri: https://{your-auth0-domain}/
        registration:
          oidc:
            client-id: {clientId}
            client-secret: {clientSecret}
            scope: openid,profile,email
jhipster:
  security:
    oauth2:
      audience: https://{your-auth0-domain}/api/v2/
```

`issuer-uri`の値に疑問がある場合は、**Applications** > **{Your Application}** > **Settings** > **Advanced Settings** > **Endpoints** > **OpenID Configuration**から値を取得できます。`.well-known/openid-configuration`のサフィックスはSpring Securityによって追加されるので削除してください。

**Applications** > **API** > **API Audience**フィールドからデフォルトの`Auth0 Management API`オーディエンス値を使用できます。独自のカスタムAPIを定義して、識別子をAPIオーディエンスとして使用することもできます。

- `Cypress`テストを実行する前に、`CYPRESS_E2E_USERNAME`および`CYPRESS_E2E_PASSWORD`環境変数を上書きして、`Auth0`ユーザーの詳細を指定してください。詳細については、[Cypressのドキュメント](https://docs.cypress.io/guides/guides/environment-variables#Setting)を参照してください。

```shell
export CYPRESS_E2E_USERNAME=<your-username>
export CYPRESS_E2E_PASSWORD=<your-password>
```

_注意_：Auth0では、ユーザーは最初のログイン時に認可の同意を提供する必要があります。同意フローは現在、Cypressテストスイートでは処理されません。この問題を軽減するには、すでに同意を付与しているユーザーアカウントを使用して、対話型ログインを介したアプリケーションアクセスを許可できます。

Cypressで認証の問題が発生した場合の回避策については、[このガイド](https://docs.cypress.io/guides/testing-strategies/auth0-authentication#Auth0-Rate-Limiting-Logins)を参照してください。

#### 環境変数の使用

環境変数を使用してのデフォルトの上書もできます。次に例を示します。

```bash
export SPRING_SECURITY_OAUTH2_CLIENT_PROVIDER_OIDC_ISSUER_URI="https://{your-auth0-domain}/"
export SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_OIDC_CLIENT_ID="{client-id}"
export SPRING_SECURITY_OAUTH2_CLIENT_REGISTRATION_OIDC_CLIENT_SECRET="{client-secret}"
export JHIPSTER_SECURITY_OAUTH2_AUDIENCE="https://{your-auth0-domain}/api/v2/"
```

これを`~/.auth0.env`ファイルに入れて`source ~/.auth0.env`を実行すると、デフォルトのKeycloak設定をAuth0でオーバーライドして、MavenまたはGradleでアプリを起動できます。登録した資格情報を使用してサインインできるはずです。

_注意_：Windowsの場合は、`source`コマンドが動作するように、[WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)をインストールする必要があります。

<a name="create-native-app-auth0"></a>
#### Auth0でモバイル用のネイティブアプリを作成する

JHipsterの[Ionic](https://github.com/jhipster/generator-jhipster-ionic)または[React Native](https://github.com/jhipster/generator-jhipster-react-native)のBlueprintを使用してモバイルアプリを開発している場合、OIDCを使用しているなら、Auth0でネイティブアプリを作成することになる可能性があります。

1. **Native**アプリケーションを作成し、次のAllowed Callback URLsを追加します。

    - Ionic: `http://localhost:8100/callback,dev.localhost.ionic:/callback`
    - React Native: `http://localhost:19006/,https://auth.expo.io/@<username>/<appname>`

2. Allowed Logout URLsを次のように設定します。

    - Ionic: `http://localhost:8100/logout,dev.localhost.ionic:/logout`
    - React: `http://localhost:19006/,https://auth.expo.io/@<username>/<appname>`

3. Allowed Origins (CORS)を設定します。

    - Ionic: `http://localhost:8100,capacitor://localhost,http://localhost`
    - React Native: `http://localhost:19006`

#### Ionicアプリをアップデートする

生成されたクライアントIDを使用するように、`ionic/src/environments/environment.ts`を更新します。`server_host`の値は、JHipsterアプリケーション（`/api/auth-info`）から検索されますが、フォールバック値としての定義もできます。また、audienceも指定する必要があります。以下は例です。

```ts
const oidcConfig: IAuthConfig = {
  client_id: '<native-client-id>',
  server_host: 'https://<your-auth0-domain>/',
  ...
};

export const environment = {
  ...
  audience: 'https://<your-auth0-domain>/api/v2/',
  ...
};
```

Ionicアプリを再起動し、Auth0でログインします！

#### Reactネイティブアプリのアップデート

クライアントIDを`app/config/app-config.js`にコピーします。

`app/modules/login/login.utils.ts`の`audience`を更新します。

```ts
audience: 'https://<your-auth0-domain>/api/v2/',
```

React Nativeアプリを再起動し、Auth0でログインします！

<!--
#### OpenID Connect Tutorials

// coming soon!
-->

<h2 id="https">HTTPS</h2>

HTTPSの使用を強制するには、次の設定を`SecurityConfiguration.java`に追加します。

```java
// Spring MVC
http.requiresChannel(channel -> channel
    .requestMatchers(r -> r.getHeader("X-Forwarded-Proto") != null).requiresSecure());
    
// WebFlux
http.redirectToHttps(redirect -> redirect
    .httpsRedirectWhen(e -> e.getRequest().getHeaders().containsKey("X-Forwarded-Proto")));
```

詳細については、Spring Securityの[Servlet](https://docs.spring.io/spring-security/site/docs/5.5.x/reference/html5/#servlet-http-redirect)と[WebFlux](https://docs.spring.io/spring-security/site/docs/5.5.x/reference/html5/#webflux-http-redirect)のドキュメントを参照してください。

これはHerokuとGoogle Cloudでテストされ、動作することが確認されています。Herokuでのプロダクションのヒントについては、[Herokuでの運用のためのSpring Bootアプリの準備](https://devcenter.heroku.com/articles/preparing-a-spring-boot-app-for-production-on-heroku)を参照してください。

<h2 id="implementation-details">実装詳細の漏洩</h2>

すべての失敗/例外は、[問題データ構造](https://github.com/zalando/problem)にマップされ、クライアントに返されます。

```json
{  
  "type": "https://www.jhipster.tech/problem/problem-with-message",
  "title": "Service Unavailable",
  "status": 503,
  "detail": "Database not reachable"
}
```

JHipsterはデフォルトではスタックトレースを含んでいませんが、`detail`には例外の`message`が含まれ、APIを介して公開されたくない[技術的詳細](https://github.com/jhipster/generator-jhipster/issues/12051)
が表れてしまう可能性があります。

```json
{  
  "type": "https://www.jhipster.tech/problem/problem-with-message",
  "title": "Bad Request",
  "status": 400,
  "detail": "JSON parse error: Cannot deserialize instance of 
       `java.util.LinkedHashMap<java.lang.Object,java.lang.Object>` out of VALUE_NUMBER_INT token; nested exception is com.fasterxml.jackson.databind.exc.MismatchedInputException: Cannot deserialize instance of `java.util.LinkedHashMap<java.lang.Object,java.lang.Object>` 
       out of VALUE_NUMBER_INT token\n at [Source: (PushbackInputStream); line: 1, column: 1]"
}
```

これを防ぐために、JHipsterは、実装の詳細の漏れを軽減するための専用のメカニズムを提供します。

* 既知の例外をチェックし、メッセージを一般的なメッセージに置き換えます（例：`Unable to convert http message`）。
* メッセージに潜在的なパッケージ名（例：`java.`または`.org`）が含まれているかどうかをチェックし、メッセージを一般的なもの（例：`Unexpected runtime exception`）で置き換えます。

ログには依然として詳細な例外が含まれているため、外部からの攻撃者がAPIを悪用して貴重な技術的詳細を得ることができない間に、
実際の問題を特定できます（訳注：miusing→misusing）。

ロジックを変更する必要がある場合（メッセージに技術的な詳細が含まれていても検出されなかった場合など）は、
必要なロジックを`ExceptionTranslator.java`の`prepare`メソッドに追加することで変更できます。
