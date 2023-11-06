---
layout: default
title: JHipsterドメイン言語 - エンティティとフィールド
permalink: /jdl/entities-fields
sitemap:
    priority: 0.5
    lastmod: 2019-10-27T12:00:00-00:00
---

# <i class="fa fa-star"></i> JHipsterドメイン言語(JDL) - エンティティ

## 概要

1. [構文](#構文)
1. [例](#例)
   1. [基本の例](#基本の例)
   1. [カスタム・テーブル名](#カスタムテーブル名)
   1. [フィールド](#フィールド)
   1. [フィールド検証](#フィールド検証)
   1. [Blob宣言](#blob宣言)
   1. [正規表現](#正規表現)
   1. [コメント](#コメント)
1. [フィールドタイプと検証](#フィールドタイプと検証)

---

### 構文

エンティティの宣言は次のように行われます。
```
[<entity javadoc>]
[<entity annotation>*]
entity <entity name> [(<table name>)] {
  [<field javadoc>]
  [<field annotation>*]
  <field name> <field type> [<validation>*]
}
```

  - `<entity name>` エンティティの名前
  - `<field name>` エンティティのフィールドの名前
  - `<field type>` JHipsterがサポートするフィールドの型
  - オプションとして以下があります。
    - `<entity javadoc>` エンティティのドキュメント
    - `<entity annotation>` エンティティのオプション（使用可能なオプションの完全なリストについては、[オプション][]を参照）
    - `<table name>` データベーステーブル名（エンティティ名から自動的に計算された名前とは別のものを指定する場合）
    - `<field javadoc>` フィールドのドキュメント
    - `<field annotation>` フィールドのオプション
    - `<validation>` フィールドの検証


---

### 例

#### 基本の例

```jdl
entity A
```

これは以下と同じです。

```jdl
entity A(a) {}
```

前者は、"body"（フィールドの中括弧）とテーブル名を指定しない、より単純な形式です。

---

#### カスタム・テーブル名

カスタムテーブル名の指定もできます。

```jdl
 entity A(my_super_entity)
```

---

#### フィールド

```jdl
entity A {
  name String required
  age Integer
}
```

---

#### フィールド検証

```jdl
entity A {
  name String required
  age Integer min(42) max(42)
}
```

---

#### Blob宣言

JHipsterは、イメージ・タイプまたは任意のバイナリ・タイプのいずれかを選択できる優れた選択肢を提供します。JDLでも同じことができます。
エディタを使用してカスタムタイプ（DataTypeを参照）を作成し、次の規則に従って名前を付けます。
  - "any"バイナリ型のフィールドを作成するための`AnyBlob`または`Blob`
  - イメージのフィールドを作成するための`ImageBlob`
  - CLOB（ロングテキスト）のフィールドを作成するための`TextBlob`

また、DataTypeは必要な数だけ作成できます。

---

#### 正規表現

これは特別な検証で（String型でのみ使用可能）、構文は次のとおりです。

```jdl
entity A {
  name String pattern(/^[A-Z][a-z]+\d$/)
}
```

<<<<<<< HEAD
内訳を見てみましょう。
  - `pattern`は正規表現の検証を宣言するためのキーワードです（通常の括弧付き）。
  - `/.../` パターンは2つのスラッシュの内側で宣言されます。
  - `\` アンチスラッシュはエスケープする必要はありません。
=======
Let's break it down:
  - `pattern` is the keyword to declare a regex validation (with the normal parentheses)
  - `/.../` the pattern is declared inside two slashes
  - `\` anti-slashes needn't be escaped
>>>>>>> upstream/main

---

#### コメント

JDLでは、エンティティとフィールドに対してコメントを付けることができ、ドキュメント（バックエンドのJavadocまたはJSDoc
）を生成します。

```jdl
/**
 * This is a comment
 * about a class
 * @author Someone
 */
entity A {
  /**
   * This comment will also be used!
   * @type...
   */
   name String
   age Integer // this is yet another comment
}
```

これらのコメントは、後でJHipsterによってJavadocコメントとして追加されます。JDLには独自のコメントがあります。
  - // 無視されるコメント
  - /** 無視されるコメントではありません */

したがって、`//`で始まるものはすべてJDLの内部コメントと見なされ、Javadocとしてカウントされません。
`#`で始まるJDL Studioディレクティブは、構文解析中に無視されることに注意してください。

別の形式のコメントは、次のコメントです。
```
entity A {
  name String /** 凄いフィールド */
  count Integer /** その他の凄いフィールド */
}
```

ここで、Aの名前には「凄いフィールド」というコメントが付けられ、Bの名前には「その他の凄いフィールド」というコメントが付けられます。

また、カンマは必須ではありませんが、コード内でミスをしないようにカンマを使用することをお勧めします。
**カンマとその後のコメントを混在させたい場合は、注意してください!**
```
entity A {
  name String, /** 私のコメント */
  count Integer
}
```
Aのnameにはコメントが付きません。countの方にコメントが付くからです。

---

### フィールドタイプと検証

各フィールド・タイプには独自の検証リストがあります。JDLでサポートされているタイプは次のとおりです。

<table class="table table-striped table-responsive">
  <tr>
    <th>JDLタイプ</th>
    <th>検証</th>
  </tr>
  <tr>
    <td>String</td>
    <td><dfn>required, minlength, maxlength, pattern, unique</dfn></td>
  </tr>
  <tr>
    <td>Integer</td>
    <td><dfn>required, min, max, unique</dfn></td>
  </tr>
  <tr>
    <td>Long</td>
    <td><dfn>required, min, max, unique</dfn></td>
  </tr>
  <tr>
    <td>BigDecimal</td>
    <td><dfn>required, min, max, unique</dfn></td>
  </tr>
  <tr>
    <td>Float</td>
    <td><dfn>required, min, max, unique</dfn></td>
  </tr>
  <tr>
    <td>Double</td>
    <td><dfn>required, min, max, unique</dfn></td>
  </tr>
  <tr>
    <td>Enum</td>
    <td><dfn>required, unique</dfn></td>
  </tr>
  <tr>
    <td>Boolean</td>
    <td>required, unique</td>
  </tr>
  <tr>
    <td>LocalDate</td>
    <td><dfn>required, unique</dfn></td>
  </tr>
  <tr>
    <td>ZonedDateTime</td>
    <td><dfn>required, unique</dfn></td>
  </tr>
  <tr>
    <td>Instant</td>
    <td><dfn>required, unique</dfn></td>
  </tr>
  <tr>
    <td>Duration</td>
    <td><dfn>required, unique</dfn></td>
  </tr>
  <tr>
    <td>UUID</td>
    <td><dfn>required, unique</dfn></td>
  </tr>
  <tr>
    <td>Blob</td>
    <td><dfn>required, minbytes, maxbytes, unique</dfn></td>
  </tr>
  <tr>
    <td>AnyBlob</td>
    <td><dfn>required, minbytes, maxbytes, unique</dfn></td>
  </tr>
  <tr>
    <td>ImageBlob</td>
    <td><dfn>required, minbytes, maxbytes, unique</dfn></td>
  </tr>
  <tr>
    <td>TextBlob</td>
    <td><dfn>required, unique</dfn></td>
  </tr>
</table>

[オプション]: options#使用可能なオプション "Options"
