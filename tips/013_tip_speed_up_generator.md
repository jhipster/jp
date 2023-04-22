---
layout: default
title: generator-jhipsterの速度を上げる
sitemap:
priority: 0.5
lastmod: 2016-05-15T22:22:00-00:00
---

# generator-jhipsterの速度を上げる

__このTipは[@pascalgrimaud](https://github.com/pascalgrimaud)から提出されました__

**警告!** npm 3+はsymlinkを使用しているため、これらのヒントは機能しません。

generator-jhipsterを使用する場合、接続速度によっては、コマンド`npm install`に数分かかることがあります。

このヒントは、多くの場合に使用できます。

- JHipsterのデモのエクスペリエンスを向上させるため
- 開発チームの場合、`.yo-rc.json`を使用してプロジェクトをより迅速に再生成します
- 継続的インテグレーション

## node_modulesの新しいプロジェクトを作成する

すべての`node_modules`ライブラリを含むディレクトリを作成し、その中に移動します。

```
mkdir jhipster-speedup
cd jhipster-speedup
```

ディレクトリ`node_modules`を作成します。

```
mkdir -p node_modules
```

プロジェクト構造は次のとおりです。

    jhipster-speedup
    ├── node_modules


**警告!** この次のコマンドは、あなたがJHipsterの開発者である場合にのみ使用してください。これはgenerator-jhipsterをあなたのフォークプロジェクトにリンクします。

```
npm link generator-jhipster
```

## プロジェクトの生成

新しいJHipsterプロジェクトを格納するディレクトリを作成し、そのディレクトリに移動します。

```
mkdir jhipster
cd jhipster
```

ディレクトリ`node_modules`へのリンクを作成します。

```
ln -s <your path>/jhipster-speedup/node_modules
```

新しいプロジェクトを生成して、すべての質問に回答します。

```
jhipster
```

1回目は数分かかります。

次回は既存の`node_modules`ディレクトリを使用するので、npmはすべてのライブラリをダウンロードするわけではありません。

**警告!**特定のライブラリを使用してpackage.jsonを変更する場合は、リンクを使用するのではなく、
jhipster-speedupからフォルダプロジェクトに`node_modules`をコピーする必要があります。
