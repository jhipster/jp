---
layout: default
title: Oh-My-Zshを使う
permalink: /oh-my-zsh/
redirect_from:
  - /oh-my-zsh.html
sitemap:
    priority: 0.7
    lastmod: 2016-07-25T18:40:00-00:00
---

# <i class="fa fa-terminal"></i> Oh-My-Zshを使う

LinuxまたはMac OS Xを使用している場合は、[Oh-My-Zsh](http://ohmyz.sh/)はZSHの設定を管理するための優れたツールです。

JHipster開発チームのほとんどはOh-My-Zshを使用しており、端末でショートカットを使用している人を見ると、ここから魔法が生まれているのです！

## Oh-My-Zsh JHipsterプラグイン

JHipster Oh-My-ZshプラグインはGithubの[https://github.com/jhipster/jhipster-oh-my-zsh-plugin](https://github.com/jhipster/jhipster-oh-my-zsh-plugin)にあります。

現在はショートカットを加えるのみですが（全てのリストは[こちら](https://github.com/jhipster/jhipster-oh-my-zsh-plugin/blob/main/jhipster.plugin.zsh)）自動補完を改善するためのコントリビューションを歓迎します！

公式のプラグインリストには（まだ）含まれていないので、手動でインストールする必要があります。

1. `~/.zshrc`を編集し、`jhipster`を有効にするプラグインのリストに追加します。

    `plugins=( ... jhipster )`

2. コマンドラインで、_oh-my-zsh_のカスタムプラグインディレクトリに移動し、リポジトリのクローンを作成します。

    `cd ~/.oh-my-zsh/custom/plugins && git clone https://github.com/jhipster/jhipster-oh-my-zsh-plugin.git jhipster && cd && . ~/.zshrc`

## 推奨プラグイン

`git`, `docker`, `docker-compose`プラグインはJHipsterで役立ちます。

`.zshrc`ファイルのプラグインセクションは次のようになります。

    plugins=(git docker docker-compose jhipster)

## その他のインストール方法

### Antigen

[Antigen](https://github.com/zsh-users/antigen)を使用する場合、以下のようにします。

1. `antigen bundle jhipster/jhipster-oh-my-zsh-plugin`を`.zshrc`の他のプラグインがリストされている場所に追加します。

2. Terminal/iTermを閉じて再開し**コンテキストをリフレッシュ**することによりプラグインを使用します。あるいは`antigen bundle jhipster/jhipster-oh-my-zsh-plugin`実行中のシェルで、antigenのクローンを作成し、*jhipster*をロードします。

### zgen

[zgen](https://github.com/tarjoilija/zgen)を使用する場合、以下のようにします。

1. `zgen load jhipster/jhipster-oh-my-zsh-plugin`を`.zshrc`他の`zgen load`コマンドと同じ場所に追加します。
2. `rm ${ZGEN_INIT}/init.zsh && zgen save`を実行します。
