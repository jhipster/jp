---
layout: default
title: Bootstrap 4のカスタマイズ
permalink: /customizing-bootstrap-4/
sitemap:
    priority: 0.7
    lastmod: 2017-12-08T00:00:00-00:00
---

# <i class="fa fa-css3"></i> Bootstrap 4のカスタマイズ

## 基本的なカスタマイズ

_プロの技:`npm start`を実行して、変更のフィードバックをすぐに得ることを忘れないでください!_

JHipsterアプリケーションの外観をカスタマイズする最も簡単な方法は、
`src/main/webapp/content/css/global.css`のCSSスタイルを上書きします。または、Sassオプションを選択した場合は、`src/main/webapp/content/scss/global.scss`ファイルを上書きします。

BootstrapもSassで記述されているため、Sassを使用することは、プレーンなCSSよりも簡単で、簡潔で、強力です。Bootstrapの[テーマに関する公式ドキュメント](https://getbootstrap.com/docs/4.0/getting-started/theming/)を参照してください。

自分の`scss`ファイルでBootstrapの[パーシャル](http://sass-lang.com/guide)を使用したい場合は、以下のように`scss`ファイルの先頭にインポートしてください。
たとえば、border-radius mixinを使用するには、次のように指定します。

```
@import "node_modules/bootstrap/scss/variables";
@import "node_modules/bootstrap/scss/mixins/border-radius";
```

メインのSassファイルではなく、部分的なファイルのみをインポートするようにしてください。そうしないと、重複したCSSが生成され、問題が発生する可能性があります。

色やborder-radiusなどのデフォルトのブートストラップ設定を変更するには、部分ファイル`src/main/webapp/content/scss/_bootstrap-variable.scss`でプロパティの値を追加または変更します。

Bootstrapの[_variables.scss](https://github.com/twbs/bootstrap/blob/v4-dev/scss/_variables.scss)で定義されているすべての値は、ここで上書きできます。
