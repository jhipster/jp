---
layout: default
title: Querydslサポートの追加
sitemap:
priority: 0.5
lastmod: 2017-04-27T08:40:00-00:00
---

# Querydslサポートの追加

__このTipは[@omrzljak](https://github.com/omrzljak)により提出され、[@arnaud-deprez](https://github.com/arnaud-deprez)により更新されました__

Spring Data の[クエリでできること](http://docs.spring.io/spring-data/mongodb/docs/current/reference/html/#mongodb.repositories.queries)ではクエリを作成するのに十分ではない場合があります。`@Query`アノテーションや[独自に書く](http://docs.spring.io/spring-data/mongodb/docs/current/reference/html/#mongodb.repositories.queries.json-based)こともできますが、私たちの中には、[Querydsl](http://www.Querydsl.com/)が提供するようなタイプセーフなクエリを書くのが好きな人もいます。

## 生成されたPredicateクラス

Querydslの重要な部分は、Predicateと呼ばれるクエリ用に生成されたドメインクラスです。spring-data-mongodbの場合、これらはJavaアノテーション後処理ツールによって生成されます。

## Gradleプラグイン

spring-data-mongodbの設定をサポートするQuerydsl用のGradleプラグインもあります。

## Mavenプラグイン

Maven用のプラグインもあります。Mavenの構成については、ドキュメントの[Mavenによるインテグレーション](http://www.querydsl.com/static/querydsl/latest/reference/html/ch02.html#d0e132)の章で詳しく説明されています。また、次の手順を実行する必要があります。

**注**: `org.slf4j`はSpring Bootに含まれているので、依存関係に含めないでください。

## 変更

### build.gradle

`build.gradle`で、依存関係を`Querydsl plugin`に追加します。

```groovy
buildscript {
    repositories {
        jcenter()
    }
    dependencies {
        classpath "gradle.plugin.com.ewerk.gradle.plugins:querydsl-plugin:1.0.9"
    }
}

apply from: 'gradle/querydsl.gradle'
```
`gradle.properties`で使用する`Querydsl version`を定義してください。

```properties
querydsl_version=4.1.4
```

Then create a the file `gradle/querydsl.gradle` with

```groovy
apply plugin: "com.ewerk.gradle.plugins.querydsl"

sourceSets {
    main {
        java {
            srcDir "$buildDir/generated/source/apt/main"
        }
    }
}

querydsl {
    // we use mongodb
    springDataMongo = true
    querydslSourcesDir = "$buildDir/generated/source/apt/main"
}

dependencies {
    compile "com.querydsl:querydsl-mongodb:${querydsl_version}"
    compileOnly "com.querydsl:querydsl-apt:${querydsl_version}"
}
```

__注__ MongoDBを使用していますが、Querydslプラグインは[その他のオプション](https://github.com/ewerk/gradle-plugins/tree/master/Querydsl-plugin)もサポートしています。

`gradle build`を実行すると、次のような出力が表示されます。
`Note: Generating net.jogat.names.domain.QName for [net.jogat.names.domain.Name]`

@Documentでアノテートされたドメインクラスごとに、Querydslプラグインは1つのPredicateクラスを生成します。

## リポジトリクラスの変更

例えば`Name`のようなドメインクラスがある場合は、`NameRepository`クラスもあります。すべてのリポジトリクラスを`QueryDslPredicateExecutor`から拡張するように変更する必要があります。

    public interface NameRepository extends MongoRepository<Name, String>, QueryDslPredicateExecutor<Name> {

これにより、Querydslをサポートする追加のメソッドでリポジトリクラスが拡張されます。 ([参考](http://docs.spring.io/spring-data/mongodb/docs/current/reference/html/#mongodb.repositories.queries.type-safe) )

## Webサポート

パラメータ化されたリクエストをサポートするために残りのコントローラを拡張するには、`org.springframework.data.querydsl.binding.QuerydslPredicate`でアノテーションが付けられた`com.mysema.query.types.Predicate`をメソッドパラメータに追加する必要があります。

    @RestController
    @RequestMapping("/api")
    class NameResource {

        private final NameRepository nameRepository;
        
        public NameResource(NameRepository nameRepository) {
            this.nameRepository = nameRepository;
        }

        @RequestMapping(value = "/names",
            method = RequestMethod.GET,
            produces = MediaType.APPLICATION_JSON_VALUE)
        @Timed
        public ResponseEntity<List<Name>> getAllNames(@QuerydslPredicate(root = Name.class) Predicate predicate,
                                                        Pageable pageable) {
            log.debug("REST request to get a page of Name");
            Page<Name> page = nameRepository.findAll(predicate, pageable);
            HttpHeaders headers = PaginationUtil.generatePaginationHttpHeaders(page, "/api/names");
            return new ResponseEntity<>(page.getContent(), headers, HttpStatus.OK);
        }
        ...
    }

また、`NameResourceIntTest`では`QuerydslPredicateArgumentResolver`をサポートする必要があります。

    public class NameResourceIntTest {
        ...
        @Autowired
        private NameRepository nameRepository;
        @Autowired
        private QuerydslPredicateArgumentResolver querydslPredicateArgumentResolver;

        @PostConstruct
        public void setup() {
            MockitoAnnotations.initMocks(this);
            NameResource nameResource = new nameResource(nameRepository);
            this.restNameMockMvc = MockMvcBuilders.standaloneSetup(nameResource)
                .setCustomArgumentResolvers(pageableArgumentResolver, querydslPredicateArgumentResolver)
                .setMessageConverters(jacksonMessageConverter).build();
        }
        ...
    }

詳細については、[ドキュメント](http://docs.spring.io/spring-data/mongodb/docs/current/reference/html/#core.web.type-safe)を参照してください。

## タイプセーフなクエリを作成する

GradleまたはMavenプラグインは、Name.classのクエリを記述するために使用できるクラスQNameを生成します。次にJavaの例を示します。

```java
QName name = QName.name;

// リスト"categorie"に文字列"TOP_EVER"が含まれるすべての名前をカウントします
nameRepository.count(name.categories.contains("TOP_EVER"));
```
