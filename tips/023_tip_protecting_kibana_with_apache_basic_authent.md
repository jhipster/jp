---
layout: default
title: Apache（ベーシック認証）でKibanaを保護する
sitemap:
priority: 0.5
lastmod: 2018-01-31T14:10:00-00:00
---

# Apache（ベーシック認証）でKibanaを保護する

このTipは[@raiden0610](https://github.com/raiden0610)によって提出されました。

## mod_proxyをアクティブにする

    a2enmod proxy
    a2enmod proxy_http
    a2enmod headers

    service apache2 restart

<<<<<<< HEAD
## Vitualhost構成
使用しているディストリビューションに応じて、virtualhost 443または80の設定がどこにあるかを確認します。
=======
## Virtualhost configuration
Find where your virtualhost 443 or 80 config is, depending on your distros.
>>>>>>> upstream/main

たとえば、Ubuntu 16.04では、設定は **/etc/apache2/sites-availables** ディレクトリの **000-default-le-ssl.conf** ファイルにあります。

SSLを使用しない場合は、ファイル**000-default.conf**を参照してください。

ファイルを編集し、virtualhost 443または80のセクションに次のように貼り付けます。

    # ポート5601でのKibanaリスニングのプロキシ化
    ProxyPreserveHost On
    ProxyRequests On
    ProxyPass / http://localhost:5601/
    ProxyPassReverse / http://localhost:5601/
    
    # ベーシック認証による保護
    <Location />
            AuthType Basic
            AuthName "Restricted Content"
            AuthUserFile /etc/apache2/.htpasswd
            Require valid-user
       </Location>

Apacheの設定を再ロードします。

    service apache2 reload
    
## ユーザー名/パスワードの生成

    htpasswd /etc/apache2/.htpasswd your_user
    
## SSLのアクティブ化
次のチュートリアルに従います（ディストリビューションを選択できます）。[Let's encrypt - Certbot](https://certbot.eff.org/)（訳注：ditros→distros）

Certbotは、ApacheのSSL設定を自動的に処理します。

<div class="alert alert-warning"><i>警告:</i>
<b>ファイアウォールでポート5601を閉じることを忘れないでください。</b>そうしないと、ポート5601で基本認証なしでKibanaにアクセスできてしまいます。
</div>

これで、https://mydomain.com や http://mydomain.com でKibanaに安全にアクセスできるようになりました。