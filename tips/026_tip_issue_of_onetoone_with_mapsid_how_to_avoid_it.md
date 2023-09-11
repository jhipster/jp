---
layout: default
title: @MapsIdとの@OneToOneの問題と回避方法
sitemap:
priority: 0.1
lastmod: 2019-03-05T18:20:00-00:00
---

# @MapsIdとの@OneToOneの問題と回避方法

__このTipは[@pmverma](https://github.com/pmverma)により提出されました__

以下は、`@MapsId`で`@OneToOne`を使用することに関する既知の問題と、それを回避するためのいくつかのヒントです。
### 問題
`@OneToOne @MapsId`で`User`に関連付けられた`Preference`クラスがあるとします。
```
class Preference {
        @OneToOne
        @MapsId
        private User user;
}
```
通常JHipsterでは、以下のようになります。
1. ユーザーの`preference`を追加する場合は、データを入力し、ドロップダウンからユーザー`user01`ログインを選択して保存します。
2. 同じ`preference`を編集する場合でも、ユーザを選択するオプションがあります。今回`user02`を選択すると、バックエンド側では、リクエストのライフタイム全体にわたって`preference`オブジェクトに`user02`が保持されます。
3. 再び同じ`preference`をリロードすると、`user02`ではなく`user01`が存在することがわかります。

<<<<<<< HEAD
この間違った部分は、
**no.2ステップの`preference`オブジェクトの`user02`** です。`preference` ユーザーオブジェクトは、常に`user01`を参照する必要があります。

詳細については、[https://github.com/jhipster/generator-jhipster/issues/9100](https://github.com/jhipster/generator-jhipster/issues/9100)を参照してください。

### 回避するためのヒント

* ドロップダウンを非表示にして、現在のユーザを`preference`に **クライアント側で** プログラム的に設定します（改めて、この種の解決策は、ユーザを選択するためのドロップダウンが意味をなさない、プリファレンス、設定、ユーザプロファイルなどのエンティティに対してのみ有効です）。
* ドロップダウンを非表示にして、現在のユーザを`preference`に **サーバ側で** プログラム的に設定します（改めて、この種の解決策は、ユーザを選択するためのドロップダウンが意味をなさない、プリファレンス、設定、ユーザプロファイルなどのエンティティに対してのみ有効です。JHipsterはすでに現在のユーザを取得するメソッドを提供しています）。
* そのユーザーに対してビジネスロジックを実行する前に、正しい関連付けの値を検証してロードします（改めて、ロジックが`preference.getUser()`に依存する場合にのみ必要です）。
* Hibernate 5.4.2以降を使用している場合は、正しい関連値を取得できますが、それはエンティティのマージ操作が完了した後に限られます。したがって、エンティティのマージ操作の前にビジネスロジックが実行される場合は、それを処理する必要があります。そうしないと、誤った結果を取得する可能性があります。
=======
The incorrect part here is:
 **`user02` in `preference` object in no.2 step.** The user object in `preference` should always refer to `user01`.
 
 For more information, take a look at [https://github.com/jhipster/generator-jhipster/issues/9100](https://github.com/jhipster/generator-jhipster/issues/9100)
 
 ### Tips to avoid it
 
 * Hide the dropdown and set the current user in `preference` **at client side** programmatically. (Again this kind of solution is only valid for entities such as Preference, Settings, User Profile and so on, where having a dropdown to choose user does not makes sense. )
 * Hide the dropdown and set the current user in `preference` **at server side** programmatically. (Again this kind of solution is only valid for entities such as Preference, Settings, User Profile and so on, where having a dropdown to choose user does not makes sense. JHipster have already provided a method to get current user.)
 * Validate and load the correct association value before doing any business logic on that user. (Again this is needed only if your logic depends on `preference.getUser()`
 * If you are using Hibernate 5.4.2 and later then you will get correct association value but only after entity merge operation has finished. So if your business logic is executed before entity merge operation, you have to take care of it otherwise you might get incorrect results.
>>>>>>> upstream/main
