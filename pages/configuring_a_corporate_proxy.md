---
layout: default
title: 企業向けプロキシの設定
permalink: /configuring-a-corporate-proxy/
redirect_from:
  - /configuring_a_corporate_proxy.html
sitemap:
    priority: 0.7
    lastmod: 2016-08-18T08:00:00-00:00
---

# <i class="fa fa-exchange"></i> 企業向けプロキシの設定

JHipsterを企業内で使用する場合、企業内プロキシをバイパスするように全てのツールを設定する必要があります。

`HTTP_PROXY`と`HTTPS_PROXY`の環境変数を設定するか、または[Cntlm](http://cntlm.sourceforge.net/)のようなツールを使う方法があります。

しかし、これだけではおそらく不十分で、JHipsterで使用するすべてのツールを個別に設定する必要があります。

## はじめに

以下のようなプロキシが定義されているとします。

- ユーザー名
- 暗号
- ホスト
- ポート

結果としての設定は、`http://username:password@host:port`です。

[Cntlm](http://cntlm.sourceforge.net/)を使う場合は、`127.0.0.1:3128`のような設定になります。それ以外の場合は、次の手順で各ツールを個別に設定してください。

## NPMの設定

以下のコマンドを使用します。

```
npm config set proxy http://username:password@host:port
npm config set https-proxy http://username:password@host:port
```

または、`~/.npmrc`ファイルを直接編集してください。

```
プロキシ=http://username:password@host:port
https-proxy=http://username:password@host:port
https_proxy=http://username:password@host:port
```

## Npmの設定

以下のコマンドを使用します。

```
npm config set proxy http://username:password@host:port
npm config set https-proxy http://username:password@host:port
```

## Gitの設定

以下のコマンドを使用します。

```
git config --global http.proxy http://username:password@host:port
git config --global https.proxy http://username:password@host:port
```

または、`~/.gitconfig`ファイルを直接編集してください。

```
[http]
        proxy = http://username:password@host:port
[https]
        proxy = http://username:password@host:port
```

## Mavenの設定

`~/.m2/settings.xml`ファイルの`proxies`セッションを編集します。

```
<proxies>
    <proxy>
        <id>id</id>
        <active>true</active>
        <protocol>http</protocol>
        <username>username</username>
        <password>password</password>
        <host>host</host>
        <port>port</port>
        <nonProxyHosts>local.net|some.host.com</nonProxyHosts>
    </proxy>
</proxies>
```

### Maven Wrapper

プロジェクトフォルダ内に`.mvn/jvm.config`というファイルを新規作成し、以下のようにプロパティを設定します。

```
-Dhttp.proxyHost=host 
-Dhttp.proxyPort=port 
-Dhttps.proxyHost=host 
-Dhttps.proxyPort=port 
-Dhttp.proxyUser=username 
-Dhttp.proxyPassword=password
```

## Gradleの設定

プロキシ経由でラッパーをダウンロードしている場合は、`gradle.properties`ファイルと`gradle/wrapper/gradle-wrapper.properties`ファイルに以下を追加します。

これらのプロパティをグローバルに設定したい場合は、`USER_HOME/.gradle/gradle.properties`ファイルに追加します。

```
## Proxy setup
systemProp.proxySet="true"
systemProp.http.keepAlive="true"
systemProp.http.proxyHost=host
systemProp.http.proxyPort=port
systemProp.http.proxyUser=username
systemProp.http.proxyPassword=password
systemProp.http.nonProxyHosts=local.net|some.host.com

systemProp.https.keepAlive="true"
systemProp.https.proxyHost=host
systemProp.https.proxyPort=port
systemProp.https.proxyUser=username
systemProp.https.proxyPassword=password
systemProp.https.nonProxyHosts=local.net|some.host.com
## end of proxy setup
```

## Docker

### Native Docker

OSによっては、特定のファイル（`/etc/sysconfig/docker`または`/etc/default/docker`）を編集する必要があります。

その後、dockerサービスを`sudo service docker restart`により再起動します。 

systemdに適用されることはありません。この[dockerのページ](https://docs.docker.com/engine/admin/systemd/#http-proxy)を参照して、
プロキシを設定してください。

### docker-machineによるDocker

以下のコマンドでdocker-machineを作成できます。

```
docker-machine create -d virtualbox \
    --engine-env HTTP_PROXY=http://username:password@host:port \
    --engine-env HTTPS_PROXY=http://username:password@host:port \
    default
```

あるいは`~/.docker/machine/machines/default/config.json`を編集してください。
