---
layout: default
title: WindowsでのJenkins 1のセットアップ
permalink: /setting-up-ci-windows/
redirect_from:
  - /setting_up_ci_windows.html
sitemap:
    priority: 0.7
    lastmod: 2015-01-09T12:40:00-00:00
---

# <i class="fa fa-stethoscope"></i> WindowsでのJenkins 1のセットアップ

## Jenkinsのインストール

Jenkins Windowsインストーラを[https://jenkins.io/](https://jenkins.io/)からダウンロードします。

インストーラは、SYSTEMユーザを使用してサービスとして実行するようにJenkinsを設定しますが、これは危険である可能性があるため、ユーザのサービスを特権のないものに変更する方が安全です。

[http://antagonisticpleiotropy.blogspot.fr/2012/08/running-jenkins-in-windows-with-regular.html](http://antagonisticpleiotropy.blogspot.fr/2012/08/running-jenkins-in-windows-with-regular.html)

## Jenkinsの設定

### JDK 8のインストール

Jenkins管理を通じて、JDK 8自動インストーラを追加します。

### Mavenのインストール

Jenkinsの管理ページで、ApacheのサイトからMaven自動インストーラを追加します。

### PhantomJSのインストール

バイナリを[http://phantomjs.org/download.html](http://phantomjs.org/download.html)からインストールします。

実行可能ファイルがPATHに含まれていることを確認します。

~~~
phantomjs --version
2.1.1
~~~

## NodeJSのインストール

Jenkins NodeJSプラグインはWindowsでは動作しないので、手動でインストールします。

最新のLTS（Long Term Support）64-bitバージョンを[http://nodejs.org/](http://nodejs.org/)からダウンロードします。

NodeJSをデフォルトのディレクトリ`C:\Program Files\nodejs`にインストールしないでください。これには管理者権限が必要です。`c:\nodejs`のようなより単純なパスを使用してください。

`C:\nodejs\node_modules\npm\npmrc`を編集します。

~~~
prefix=${APPDATA}\npm
~~~

以下に置き換えます。

~~~
prefix=C:\nodejs\node_modules\npm
~~~

'C:\nodejs\node_modules\npm'フォルダをPATH環境変数に追加し、インストーラによって追加されたフォルダ'C:\Users\<user>\AppData\Roaming\npm'を削除します。

npmにはGitが必要な場合があります。[https://git-for-windows.github.io/](https://git-for-windows.github.io/)からインストールします。

BowerとGulpを追加します。

~~~
npm install -g bower gulp
bower --version
gulp --version
~~~

同じマシン上に複数のバージョンのNodeJSを持つことは便利ですが、Windowsの`nvm`に相当するものは、継続的な統合よりも開発環境に重点を置いています。そのため、ジョブに別のバージョンのNodeJSが必要な場合は、PATH変数を変更してください。
