---
layout: default
title: controllerの構築
permalink: /creating-a-spring-controller/
sitemap:
    priority: 0.7
    lastmod: 2019-02-01T00:00:00-00:00
---

# <i class="fa fa-bolt"></i> Spring controllerの構築

## はじめに

_注意：このサブジェネレータは、完全なCRUDエンティティを作成する[エンティティサブジェネレータ]({{ site.url }}/creating-an-entity/)よりもはるかに単純です。_

このサブジェネレータは、Spring MVC RESTコントローラを生成します。RESTメソッドの作成もできます。

"Foo"のSpring MVC RESTコントローラを生成するには、次のように入力します。

`jhipster spring-controller Foo`

サブジェネレータは、どのメソッドを生成するかを尋ねます。メソッド名と使用するHTTPメソッドに答えると、メソッドが生成されます。

## Spring MVC RESTコントローラをSwaggerでドキュメント化できますか?

はい！　実際にはすでに完成しています！　`dev`モードで、`管理 > API`メニューを使用してSwagger UIにアクセスし、生成されたコントローラの使用を開始します。

## Spring MVC RESTコントローラにセキュリティを追加できますか?

はい！　クラスまたはメソッドにSpring Securityの`@Secured`アノテーションを追加し、生成された`AuthoritiesConstants`クラスを使用して特定のユーザー権限へのアクセスを制限します。

## Microservice Gateway開発サーバからプロキシすることはできますか?

はい！　webpack/webpack.dev.jsのプロキシのコンテキストにサービス名を追加します。
```javascript
module.exports = (options) => webpackMerge(commonConfig({ env: ENV }), {
    devtool: 'eval-source-map',
    devServer: {
        contentBase: './target/www',
        proxy: [{
            context: [
                '/<servicename>',
                /* jhipster-needle-add-entity-to-webpack - JHipster will add entity api paths here */
                ....
```
