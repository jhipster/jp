---
layout: default
title: LinuxでのJenkins 1のセットアップ
permalink: /setting-up-ci-linux/
redirect_from:
  - /setting_up_ci_linux.html
sitemap:
    priority: 0.7
    lastmod: 2015-01-09T12:40:00-00:00
---

# <i class="fa fa-stethoscope"></i> LinuxでのJenkins 1のセットアップ

以下の手順はRed Hat/CentOSサーバ用ですが、他のLinuxディストリビューションにも適用できます。

## Jenkinsのインストール

[https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Red+Hat+distributions](https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Red+Hat+distributions)の指示に従ってください。

~~~~
sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo
sudo rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key
sudo yum install jenkins

sudo service jenkins start
~~~~

`jenkins`ユーザーが作成され、ホームディレクトリは`/var/lib/jenkins`となります。

## Jenkinsの設定

### JDK 8のインストール

Jenkinsの管理を通じて、JDK 8自動インストーラを追加します。

### Mavenのインストール

Jenkinsの管理を通じて、ApacheのサイトからMaven自動インストーラを追加します。

### NodeJSのインストール

NodeJSのグローバルなインストールもできますが、プロジェクトごとに異なるバージョンのNodeJSが必要になる可能性があります。

次の2つの代替案を提案します。お好みのものを選択してください。

#### Jenkins NodeJSプラグイン

Jenkins NodeJSプラグインをインストールします。

Jenkins管理を通じて、NodeJSインストールを追加します。

- nodejs.orgからの自動インストーラ、最新のLTS（Long Term Support）64ビットバージョンを使用します。
- インストールするグローバルnpmパッケージは、bower gulpです。

#### ローカルNodeJSインストール

次のスクリプトを使用してNodeJSをローカルにインストールし、それを使用するようにJenkins PATHを更新します。

~~~ bash
# 必要なバージョンを指定
export NODE_VERSION=4.3.1

# ダウンロード
cd /tmp
wget http://nodejs.org/dist/v$NODE_VERSION/node-v4.3.1.tar.gz
tar xvfz node-v$NODE_VERSION.tar.gz

# ビルドとインストールはローカルでのみ
cd node-v$NODE_VERSION
./configure --prefix=/var/lib/jenkins/node-v$NODE_VERSION && make && make install

# nodeおよびnpmのバージョンを検査
export PATH=/var/lib/jenkins/node-v$NODE_VERSION/bin:$PATH
node --version
# v4.3.1
npm --version
# 3.7.5

# ツールをインストール
npm install -g bower gulp
bower --version
# 1.7.7
gulp --version
# 3.9.1
~~~

必ずJenkins PATHを更新してください。
