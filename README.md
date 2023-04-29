# JHipsterの公開[Webサイト（日本語）](https://www.jhipster.tech/jp/) のソースです

- 本家のWebサイト： https://www.jhipster.tech/
- 本家のリポジトリ： https://github.com/jhipster/jhipster.github.io 
- [日本語訳について](#日本語訳について)

**Note**:スタイルを変更する場合は、`css/scss`以下にある`.scss`ファイルを更新し、`npm run sass`を実行してCSSを生成してください。CSSを直接更新しないでください。

このWebサイトはGitHub Pagesでレンダリングされています。

ローカルで実行する場合は以下のとおりです。

- [ここをForkして](https://github.com/jhipster/jhipster.github.io/fork) リポジトリを作成し、あなたのファイルシステムにクローンします
- [Jekyllをインストールしてください](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/)
- 初めての場合は、`npm install && bundle install`を実行します
- システムディレクトリへのインストールを避けたい場合は、代わりに`bundle install --path vendor/bundle`によってvendorディレクトリにインストールします
- Mac OSで`nokogiri`のインストールがうまくいかない場合は、`bundle config build.nokogiri  -use-system-libraries=true --with-xml2-include="$(xcrun --show-sdk-path)"/usr/include/libxml2` を試してください
- リポジトリをクローンしたフォルダで `bundle exec jekyll serve` または `npm start` を実行します
- http://localhost:4000 からアクセスできるようになります

（Windows環境では推奨）DockerとDocker-Composeで実行する場合は以下のとおりです。

- [ここをForkして](https://github.com/jhipster/jhipster.github.io/fork) リポジトリを作成し、あなたのファイルシステムにクローンします
- `docker-compose up`を実行します
- http://0.0.0.0:4000 からアクセスできるようになります


# 日本語訳について
本サイトの日本語訳にあたっては、OSS活動へも使用可能な[みんなの自動翻訳＠TexTra®](https://mt-auto-minhon-mlt.ucri.jgn-x.jp/)の翻訳内容を活用させていただきました。この場を借りてお礼を申し上げます。

翻訳の文体は、本家のpackage.jsonにtextlintパッケージを加えての指摘と、TexTraの翻訳内容になるべく従うことで、統一させています。

誤訳や不自然な言い回しが無いよう、注意しながら進めてはいますが、もし問題がありましたら、Issue/PRでご指摘ください。

## 本家の追従方法
本家の更新に伴う日本語訳の追従については、ReactやVueの翻訳での実績がある、[オープンソースドキュメント翻訳プラットフォームとしての GitHub](https://zenn.dev/smikitky/articles/0d250f7367eda9)の運用方法がとても素晴らしく、参考にしています。この場を借りてお礼を申し上げます。

運用方法は以下の通りです。
- [Github Actions](https://github.com/jhipster/jp/actions/workflows/sync-upstream.yml)で以下を処理
  - 定期的に本家の`main`をチェック
  - 更新があれば翻訳用`sync`ブランチを作成
  - 本家の差分を翻訳中（コンフリクトマーカー有）状態として`sync`へコミット
  - `sync`を`main`にマージするプルリクエストを作成
- 翻訳者がプルリクエストの内容を確認し、`sync`の内容を翻訳しコミット
- `main`にマージ

## ページ表示
本家と同様、Github Pagesを使って表示します。表示元は`gh-pages`ブランチの内容になります。

`gh-pages`はほぼ全て`main`ブランチと同様ですが、ごく一部、日本語サイト表示のために`gh-pages`のみ変更した内容があります。
`main`との差分は[こちら](https://github.com/jhipster/jp/compare/main...gh-pages)を見て確認してください。
`main`に書かない理由は、本家のサイトの構造上、`main`に入れるとローカルのテスト環境で動かないためです。
結果、本家との差分が`main`と`gh-pages`で散在しまいますが、`gh-pages`の変更箇所は大幅なサイトの変更がない限りほぼ更新することはないので、しばらくこの構造で運用していきます。
