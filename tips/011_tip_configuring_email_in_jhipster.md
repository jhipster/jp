---
layout: default
title: メールを設定する - Gmailなど
sitemap:
priority: 0.5
lastmod: 2021-03-18T19:48:00-00:00
---
# メールを設定する - Gmailなど...

__このTipは[@RawSanj](https://github.com/RawSanj)から提出されました__

_目標：_ 以下のメール設定を使用すると、デフォルトのJHipsterアプリケーションがGmail、Outlook、またはYahooから電子メールを送信するように設定されます。

まず、`jhipster`を使用してJHipsterを実行し、新しいアプリケーションを作成するか、既存のJHipster生成アプリケーションを使用します。

## '送信元'アドレスを設定

`src\main\resources\config\application.yml`を開き、`jhipster.mail.from`プロパティを編集します。

_application.yml_
    
    jhipster:
        [...]
        mail:
            from: username@service_provider #このフィールドをspring.mail.usernameに使用される値で置き換えます。
        [...]

この手順を省略すると、電子メールがスパムとしてマークされる可能性があります。

## アプリケーションに対して、次のいずれかのEメールサービスを選択してください:

### 1.Eメール設定 - Gmail

`src\main\resources\config\application-dev.yml`に移動し、次のGmail設定を使用するようにアプリケーションを変更します。

_application-dev.yml_

    spring:
        profiles:
            active: dev
        mail:
            host: smtp.gmail.com
            port: 587
            username: gmailuserid@gmail.com  #このフィールドをGmailのユーザー名に置き換えます。
            password: ************           #このフィールドをGmailのパスワード/Appのパスワードに置き換えます。
            protocol: smtp
            tls: true
            properties.mail.smtp:
                auth: true
                starttls.enable: true
                ssl.trust: smtp.gmail.com
            [...]

Gmailのパスワードに上記の設定を使用する場合は、[セキュリティレベルの低いアプリケーションを許可](https://support.google.com/accounts/answer/6010255?hl=en)する必要があります。
設定は単純ですが、セキュリティは低くなります。また、セキュリティの低いアプリを許可することで、
Gmailで二要素認証の使用ができなくなります。

そのため、Gmailのパスワードではなく、アプリのパスワードを使用することを強くお勧めします。以下のGmailを参照してください。
この設定方法の詳細については、設定文書を参照してください。

[https://support.google.com/accounts/answer/185833](https://support.google.com/accounts/answer/185833)

これにより、二要素認証を使用できるだけでなく、「セキュリティの低いアプリケーションを許可する」オプションをオフに保つことができます。
GmailでOAuth2も使用でき、その設定方法は次の文書でハイライトされています。

[https://javaee.github.io/javamail/OAuth2](https://javaee.github.io/javamail/OAuth2)     

### 2.メール設定-Outlook.com

`src\main\resources\config\application-dev.yml`に移動し、次のOutlook構成を使用するようにアプリケーションを変更します。

_application-dev.yml_

    spring:
        profiles:
            active: dev
        mail:
            host: smtp-mail.outlook.com
            port: 587
            username: outlookuserid@outlook.com  #このフィールドをOutlookのユーザー名に置き換えます。
            password: ************               #このフィールドをOutlookのパスワードに置き換えます。
            protocol: smtp
            tls: true
            properties.mail.smtp:
                auth: true
                starttls.enable: true
                ssl.trust: smtp-mail.outlook.com
            [...]
__注__ :会社のOutlookアカウントから電子メールを送信する場合は、`emea.mycompany.com`のように、`host`を会社のMicrosoft Exchange Serverとして設定します。また、`username`を会社から提供されたシステムの標準ID（ドメイン/ユーザー名）として設定し、`password`をシステムパスワードとして設定します。
会社のOutlookの場合、**spring.mail**の`username`プロパティは、**jhipster.mail**の`from`プロパティと一致する必要があります。（訳注：Markdownがおかしくなっていますがあえてそのまま翻訳）

___ヒント___ : `Microsoft Exchange Server`を検索するには：Outlookを開き、ツールをクリックし、アカウント設定をクリックして、Microsoft Exchange（電子メールタブ以降）をダブルクリックし、Microsoft Exchange Serverのアドレスをコピーします。


### 3.Eメール設定 - Yahoo

`src\main\resources\config\application-dev.yml`に移動し、次のYahoo設定を使用するようにアプリケーションを変更します。

_application-dev.yml_

    spring:
        profiles:
            active: dev
        mail:
            host: smtp.mail.yahoo.com
            port: 587
            username: yahoouserid@yahoo.com  #このフィールドをYahooのユーザー名に置き換えます。
            password: ************           #このフィールドをYahooパスワードに置き換えます。
            protocol: smtp
            tls: true
            properties.mail.smtp:
                auth: true
                starttls.enable: true
                ssl.trust: smtp.mail.yahoo.com
            [...]

    jhipster:       
        mail:
            from: yahoouserid@gmail.com  #このフィールドをGmailのユーザー名に置き換えます。
            [...]
__注__ : Yahoo Mailの場合、**spring.mail**の`username`プロパティは**jhipster.mail**の`from`プロパティと一致する必要があります。


### 4.Eメール設定 - Zoho

`src\main\resources\config\application-dev.yml`に移動し、次のZoho設定を使用するようにアプリケーションを変更します。

_application-dev.yml_

    spring:
        profiles:
            active: dev
        mail:
            host: smtp.zoho.com
            port: 587
            username: zohouserid@zoho.com   #このフィールドをZohoのユーザー名に置き換えます。
            password: ************          #このフィールドをZohoのパスワードに置き換えます。
            protocol: smtp
            tls: true
            properties.mail.smtp:
                auth: true
                starttls.enable: true
                ssl.trust: smtp.zoho.com
            [...]


### 4. Eメール設定 - AWS SES

`src\main\resources\config\application-dev.yml`に移動し、次のAWS SES設定を使用するようにアプリケーションを変更します。

_application-dev.yml_

    spring:
        profiles:
            active: dev
        mail:
            host: email-smtp.us-east-1.amazonaws.com
            port: 465
            username: ********************
            password: ********************************************
            protocol: smtps
            debug: true
            properties.mail.smtp:
                starttls.enable: true
                starttls.required: true
                ssl.enable: true
            properties.mail.smtps:
                auth: true


*同様に、他の電子メールサービスも設定できます。電子メールサービスのSMTPメールサーバとサーバポートを確認し、それに応じて上記のフィールドを変更してください*

___アプリケーションを実行しましょう！登録ページに移動し、有効な電子メールアドレスを指定してフォームを送信すると、上記で設定した電子メールアドレスからアクティベーション電子メールが送信されます。___

__注__:[これらの例](https://github.com/RawSanj/java-mail-clients)を使用すると、資格情報を使用してテスト電子メールを送信できます。
