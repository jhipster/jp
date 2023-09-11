---
layout: default
title: Internet Explorerをサポートする
sitemap:
priority: 0.1
lastmod: 2019-03-05T18:20:00-00:00
---

# Internet Explorerをサポートする

**このTipは[@wmarques](https://github.com/wmarques)** と[@anthony-o](https://github.com/anthony-o) により提出されました。

JHipsterは、エバーグリーンブラウザのみをサポートします。
ただし、Internet Explorerなどの一部の古いブラウザは簡単にサポートできます。

そのためには、次のことを行う必要があります。

1. `tsconfig`でターゲットを`es5`に設定します。
2. 次に、2つの選択があります。
  1. 'core-js'から正しいポリフィルを追加します。使用すべきポリフィルがわからない場合は、Angular CLIプロジェクトとそのポリフィルを確認してください。
  2. または、babel + [Babel preset-env](https://babeljs.io/docs/en/babel-preset-env#usebuiltins)を使用して、browserslistファイルに基づいて正しいcore-jsポリフィルを自動的にインポートします。

## Babelを使用したヒント集

<<<<<<< HEAD
まず、`package.json`の依存関係に`@babel/core`、`@babel/preset-env`、`babel-loader`を追加します。`yarn`の例です。
=======
First, add those `package.json` dependencies: `@babel/core`, `@babel/preset-env` and `babel-loader`. Example with `npm`:
>>>>>>> upstream/main
```bash
npm install @babel/core @babel/preset-env babel-loader --save-dev
```
（JHipster v6.3.1で生成されたアプリケーションでIE11が動作するように、次のバージョンでテストしました
```json
    "@babel/core": "7.6.4",
    "@babel/preset-env": "7.6.3",
    "babel-loader": "8.0.6",
```
）

次に、`src/main/webapp/app/polyfills.ts`の先頭に次の行を追加します。
```ts
import 'core-js/stable';
import 'regenerator-runtime/runtime';
```

In `webpack/webpack.common.js`, after
```js
            {
                test: /manifest.webapp$/,
                loader: 'file-loader',
                options: {
                    name: 'manifest.webapp'
                }
            },
```
次の行を追加します。
```js
            {
                test: /\.js/,
                use: {
                  loader: 'babel-loader',
                  options: {
                    "presets": [
                      [
                        "@babel/preset-env",
                        {
                          "targets": {
                            "firefox": "60",
                            "ie": "11"
                          },
                          "useBuiltIns": "entry",
                          "corejs": 3
                        }
                      ]
                    ]
                  }
                },
                exclude: /@babel(?:\/|\\{1,2})runtime|core-js/,
              },
```

最後に、`tsconfig.json`と`tsconfig-aot.json`で`target`を`es5`に変更します。

詳細については、この[GitHub issue](https://GitHub.com/jhipster/generator-jhipster/issues/10184#issuecomment-541650501)と[このStackOverflowの回答](https://stackoverflow.com/a/58377002/535203)を参照してください。
