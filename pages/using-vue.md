---
layout: default
title: Vueの使用
permalink: /using-vue/
sitemap:
    priority: 0.7
    lastmod: 2019-03-27T23:41:00-00:00
---

# <i class="fa fa-html5"></i> Vueの使用
このセクションでは、JavaScriptライブラリ**Vue.js**について説明します。

## プロジェクト構造

JHipsterクライアントコードは`src/main/webapp`の下にあります。

私たちのアプリケーション構造、ファイル名、TypeScriptの規則について質問がある場合は、まずこのガイドをお読みください。

生成されたVueアプリケーションでは、[vue-class-component](https://github.com/vuejs/vue-class-component)スタイルとガイドラインに従ってTypeScriptを使用することに注意してください。

Vueルートの場合は、URLが明確で一貫性があるように、dash caseの命名規則に従います。
エンティティを生成すると、この規則に従ってルート名、ルートURL、およびREST APIエンドポイントURLが生成され、必要に応じてエンティティ名が自動的に複数化されます。

プロジェクトの主な構成は次のとおりです。

```
webapp
├── app                             - アプリケーション
│   ├── account                     - アカウント関連のコンポーネント
│   ├── admin                       - 管理関連のコンポーネント
│   ├── core                        - メインコンポーネント(Home、navbarなど)
│   ├── entities                    - 生成されたエンティティ
│   ├── locale                      - I18n/翻訳関連コンポーネント
│   ├── router                      - ルーティング設定
│   ├── shared                      - 構成、モデル、utilクラスなどの共有要素
│   ├── app.component.ts            - アプリケーションのメインクラス
│   ├── app.vue                     - アプリケーションのメインSFCコンポーネント
│   ├── constants.ts                - グローバルアプリケーション定数
│   ├── main.ts                     - インデックススクリプト、アプリケーションエントリポイント
│   └── shims-vue.d.ts
├── content                         - イメージやフォントなどの静的ファイルが格納されます。
├── i18n                            - 翻訳ファイル
├── swagger-ui                      - Swagger UIフロントエンド
├── 404.html                        - 404ページ
├── favicon.ico                     - お気に入りアイコン
├── index.html                      - 索引ページ
├── manifest.webapp                 - アプリケーションマニフェスト
└── robots.txt                      - ボットおよびWebクローラの構成
```

[エンティティサブジェネレータ]({{ site.url }}/creating-an-entity/)を使用して`Foo`という名前の新しいエンティティを作成すると、`src/main/webapp`の下に次のフロントエンドファイルが生成されます。

```
webapp
├── app                                        
│   ├── entities
│   │   └── foo                           - FooエンティティのCRUDフロントエンド
│   │       ├── foo-details.vue           - SFC構成要素の詳細
│   │       ├── foo-detail.component.ts   - 詳細ページコンポーネント
│   │       ├── foo-update.vue            - SFC構成要素を作成/更新
│   │       ├── foo-update.component.ts   - 作成/更新コンポーネントクラス
│   │       ├── foo.vue                   - エンティティメインSFCコンポーネント
│   │       ├── foo.component.ts          - Entityメインコンポーネントクラス
│   │       └── foo.service.ts            - Fooエンティティサービス
│   ├── router
│   │   └── index.ts                      - エンティティメインルートの設定
│   └── shared
│       └── model
│           └── foo.model.ts              - エンティティモデルクラス
└── i18n                                  - 翻訳ファイル
     ├── en                               - 英訳
     │   ├── foo.json                     - Foo名、フィールド、.の英語翻訳
     └── fr                               - フランス語翻訳
         └── foo.json                     - Foo名、フィールド、.のフランス語翻訳
```

デフォルトの言語変換は、アプリケーションの生成時に選択した内容に基づいて行われることに注意してください。'en'および'fr'は、ここではデモンストレーションのためにのみ示されています。

## VuexStoreを使用して保存

アプリケーションは、ストア[VuexStore](https://vuex.vuejs.org/guide/state.html)を使用して、アプリケーション内の状態を維持します。

このストアは、起動時に`app/config/config.ts:initVueXStore`に設定されます。新しい状態やミューテーションを追加するには、Vuexのドキュメントを参照してください。

アプリケーションはこのストアを使用して、次の項目を維持します。

* ユーザー認証情報
* 言語と翻訳
* 通知およびアラート情報
* アクティブなプロファイルデータ

## 認証

JHipsterは、[Vueルーター](https://router.vuejs.org/)を使用して、アプリケーションのさまざまな部分を整理します。

認証を必要とするルートに関しては、メタ`authorities`が望ましいルートで使用されます。このコンポーネントは、認証されていない、または許可されていないユーザーがルートにアクセスするのを防ぎます。

PrivateRouteでの使用例を次に示します。

``` typescript
const Routes = () => [{
      path: '/public',
      name: 'public',
      component: Public
    },
    {
      path: '/private',
      name: 'Private',
      component: Private,
      meta: { authorities: ['ROLE_USER'] }
    }];
```

このように、認証されていないユーザーは`/public`にアクセスできますが、`/private`にアクセスするには少なくともログインする必要があります。

インターセプターは、ユーザーが認証されているかどうかを知るために、`$store.getters.authenticated`ストア値を使用することに注意してください。

## 検証システム

フォームを検証するには、[Vuelidate](https://vuelidate.netlify.com/)ライブラリを使用します。検証制約の追加に加えて、いくつかのフィルタが用意されており、フォームでの完全な検証が可能です。カスタム検証は、次のように追加できます。

```typescript
import { required } from 'vuelidate/lib/validators';

const mustBeCool = (value) => value.indexOf('cool') >= 0;
const validations = {
  foo: {
    required,
    mustBeCool
  }
};
@Component({
  validations
})
export default class FooComponent extends Vue {
  foo: string = null;
}
```

## Bootswatchテーマ

Theming Bootstrapは、[Bootswatch](https://bootswatch.com)テーマを使用して直接実行できます。Bootswatchによって提供される多くのテーマの1つを選択するために、生成中に質問を提供するようにしました。
