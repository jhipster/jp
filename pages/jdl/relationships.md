---
layout: default
title: JHipsterドメイン言語 - リレーションシップ
permalink: /jdl/relationships
sitemap:
    priority: 0.5
    lastmod: 2019-11-03T12:00:00-00:00
---

# <i class="fa fa-star"></i> JHipsterドメイン言語(JDL) - リレーションシップ

## 概要

1. [リレーションシップの種類](#リレーションシップの種類)
1. [リレーションシップのメソッド](#リレーションシップのメソッド)
1. [複数のリレーションシップのボディ](#複数のリレーションシップのボディ)
1. [構文](#構文)
1. [例](#例)
   1. [基本の例](#基本の例)
   1. [注入フィールド](#注入フィールド)
   1. [結合フィールド](#結合フィールド)
   1. [メソッド](#メソッド)
   1. [オプションの使用](#オプションの使用)
   1. [必須のサイド](#必須のサイド)
   1. [再帰リレーションシップ](#再帰リレーションシップ)
   1. [コメント](#コメント)

---

### リレーションシップの種類

キーワード`relationship`の後に記述されます。

次の4つのリレーションシップタイプがあります。
  - `OneToOne`
  - `OneToMany`
  - `ManyToOne`
  - `ManyToMany`

リレーションシップについてと何を達成できるかについてもっと知りたい場合は
[専用ページ](/managing-relationships)を参照ください。

名前を複数形にすることに関する注意：JHipsterはそれらを処理するので、リレーションシップの中で処理する必要はありません。

---

### リレーションシップのメソッド

元のエンティティと先のエンティティの後に記述され、`with`キーワードとともに使用されます。

サポートされているメソッドは以下です。
- `Authority`:宛先エンティティが`User`や`builtInEntity`のような組み込みエンティティである場合に必要です

---

### 複数のリレーションシップのボディ

JDLファイルに同じタイプの _n_ 個のリレーションシップがあることにうんざりしている場合でも、心配する必要はありません。解決策はあります。

例えば、次のJDLサンプルを見てください。
```jdl
relationship OneToOne {
  A to B
}
relationship OneToOne {
  B to C
}
relationship OneToOne {
  C to D
}
relationship OneToOne {
  D to A
}
```

解決策として、次のように、リレーションシップ宣言内にすべてのリレーションシップ本体を含めることができます。
```jdl
relationship OneToOne {
  A to B,
  B to C,
  C to D,
  D to A
}
```

この構文は、次の場合に非常に役立ちます。
  - 同じタイプのリレーションシップをたくさん持っている場合
  - どのようなリレーションシップがあるかを知りたい場合
  - JDLファイルでそれらを探すために時間を無駄にしたくない場合

---

### 構文

リレーションシップの宣言は次のように行われます。
```
relationship (OneToMany | ManyToOne | OneToOne | ManyToMany) {
  @<option>("<option value>")+ <from entity>[{<relationship name>[(<display field>)]}] to @<option>("<option value>")+ <to entity>[{<relationship name>[(<display field>)]}]+
}
```

  - `(OneToMany | ManyToOne| OneToOne | ManyToMany)`はリレーションシップのタイプです。
  - `<option>`は次の値の1つを指定します: `Id | OnDelete | OnUpdate`。これをリレーションシップの正しい側に置くようにしてください。最初の文字の大文字と小文字は区別されません（jdlのエクスポート時は大文字が生成されます）。
  - `<option value>` はオプションに適合する値の1つを指定します。 `NO ACTION | RESTRICT | CASCADE | SET NULL | SET DEFAULT`
  - `<from entity>`は、リレーションシップのエンティティの所有者の名前です：いわゆる「元」です。
  - `<to entity>`は、リレーションシップの先となるエンティティの名前です：いわゆる「先」です。
  - `<relationship name>`は、もう一方の端をタイプとするフィールドの名前です。
  - `<display field>`は、選択ボックスに表示されるフィールドの名前です（デフォルト：`id`）。
  - `required`注入されたフィールドが必須かどうか。
  - `with builtInEntity`は、関係の宛先が組み込みエンティティーかどうか。
  - 複数のリレーションシップ主体を持つことができます。
    - 詳細については、[複数のリレーションシップのボディ](#複数のリレーションシップのボディ)セクションを参照してください。

---

### 例

#### 基本の例

```jdl
relationship OneToOne {
  A to B
}
```

この例は以下の例と同じです。
```jdl
relationship OneToOne {
  A{b} to B{a}
}
```
注入されたフィールドを指定しないことで、短い形式で双方向のリレーションシップを持たせます。

別の例です。
```jdl
relationship OneToOne {
  A{b} to B
}
```
これにより、単一方向のリレーションシップが生成されます。エンティティBはエンティティAを介してのみ探索できますが、エンティティAはエンティティBを介して探索できません。


---

#### 注入フィールド

```jdl
relationship ManyToMany {
  A{b} to B{a}
}
```

これは双方向のリレーションシップです。つまり、両方のエンティティがもう一方のエンティティの「インスタンス」を持って
生成されます。

---

---

#### メソッド

```jdl
relationship OneToOne {
  A to User with builtInEntity
}
```

---

#### オプションの使用

```jdl
relationship ManyToOne {
   A to @OnDelete("SET NULL") @OnUpdate("CASCADE") B
}
```

---

#### 必須のサイド

少なくとも1つのリレーションシップサイドを必須にするために使用します。

```jdl
relationship ManyToMany {
  A{b required} to B{a}
}

// または

relationship ManyToMany {
  A{b} to B{a required}
}

または

relationship ManyToMany {
  A{b(name) required} to B{a required}
}
```

---

#### 再帰リレーションシップ

再帰リレーションシップは、元と先のエンティティが同じリレーションシップです。

```jdl
relationship ManyToMany {
  A{parent} to A{child}
}
```

---

#### 必須な再帰リレーションシップに関する注意

[ここ](https://github.com/jhipster/generator-jhipster/issues/11495)で指摘されているように、同じエンティティとの必須なリレーションシップ
はサポートされていません。必須とは、子は**常に**親を持たなければならず、親も常に親を持たなければならない、といったことです。
可能な回避策は、明示的なルートおよび子エンティティを持つことです。

----

#### コメント

リレーションシップにコメントを追加できます。

```jdl
relationship OneToOne {
  /** このコメントはエンティティAのbの前に置かれます*/
  A{b}
  to
  /** このコメントはエンティティBのaの前に置かれます*/
  B{a}
}
```

ここでもこれまでと同じコメント規則が適用されます。
これらのコメントは、後でJHipsterによってJavadocコメントとして追加されます。JDLには独自のコメントがあります。
  - // 無視されるコメント
  - /** 無視されるコメントではありません */

したがって、`//`で始まるものはすべてJDLの内部コメントと見なされ、Javadocとしてカウントされません。
`#`で始まるJDL Studioディレクティブは、構文解析中に無視されることに注意してください。
