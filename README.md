# JHipsterの公開[Webサイト](https://www.jhipster.tech/) のソースです

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

