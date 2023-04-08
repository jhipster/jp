---
layout: default
title: Jenkins 2での継続的インテグレーションのセットアップ
permalink: /setting-up-ci-jenkins2/
redirect_from:
  - /setting_up_ci_jenkins2.html
sitemap:
    priority: 0.7
    lastmod: 2017-01-19T14:15:00-00:00
---

# <i class="fa fa-stethoscope"></i> Jenkins 2での継続的インテグレーションのセットアップ

## Jenkins 2のインストール

### 標準

マシンにJDK 8をインストールします。

公式サイト[https://jenkins.io/2.0/](https://jenkins.io/2.0/)に行き

`jenkins.war`をダウンロードします。

### Dockerの場合

[Dockerイメージ](https://hub.docker.com/r/jenkins/jenkins)を起動します。
(_JHipsterアプリケーションが8080で実行するように設定されているため、デフォルトのポートは18080に変更されています_)

`docker container run -d --name jenkins2 -p 18080:8080 -p 50000:50000 jenkins/jenkins`

その後、Jenkinsのダッシュボードにアクセスできます。
- http://localhost:18080（MacOSおよびLinuxの場合）
- http://192.168.99.100:18080（Windowsの場合）
  - これがうまくいかない場合は、`192.168.99.100`をあなたのDockerのデフォルトのIPアドレス`docker-machine ip default`に置き換えてください。

注：`initialAdminPassword`を入力するよう求められます。パスワードはコンテナの起動時にログに記録されています。
`docker logs jenkins2`からもアクセスできます。
例：
```
*************************************************************
*************************************************************
*************************************************************

Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

6707db8735be4ee29xy056f65af6ea13

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

*************************************************************
*************************************************************
*************************************************************
```

## 新しいジョブの作成

- 新しいアイテムの追加
    - 項目名を入力
    - パイプラインを選択
    - OKをクリック

![Jenkins2 item]({{ site.url }}/images/jenkins2_add_item.png)

- Definition: Pipeline script from SCM
- SCM: Git
- Repositories
    - Repository URL: ここでリポジトリを選択します

![Jenkins2 pipeline]({{ site.url }}/images/jenkins2_pipeline.png)

## Jenkinsファイル

![Jenkins2 result]({{ site.url }}/images/jenkins2_result.png)
