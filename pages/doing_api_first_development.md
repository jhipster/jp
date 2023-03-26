---
layout: default
title: APIファーストな開発を行う
permalink: /doing-api-first-development/
redirect_from:
  - /doing-api-first-development.html
sitemap:
    priority: 0.7
    lastmod: 2018-06-11T00:00:00-00:00
---

# <i class="fa fa-search"></i> APIファーストな開発を行う

JHipsterアプリケーションを生成するときに、追加のテクノロジのプロンプトが表示されたら、`API first development using OpenAPI-generator`オプションを選択できます。
このオプションは、[OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)を使用してOpenAPI(Swagger)定義ファイルからAPIコードを生成するようにビルドツールを設定します。
Swagger v2とOpenAPI v3の両方のフォーマットがサポートされています。

### APIファーストな開発が合理的である理由

APIファースト開発では、コードからドキュメントを生成するのではなく、最初に仕様を記述してからコードを生成する必要があります。
これには、次の利点があります。

- 実装の結果としてではなく、ユーザのためにAPIを設計できます。
- 新しいサーバエンドポイントがリリースされる前に仕様ファイルを使用してモックを作成できるため、フロントエンドとバックエンドの開発をより分離できます。
- OpenAPIドキュメントを使用するためのライブサーバは必要ありません。

### OpenAPIジェネレータプラグインの使用

OpenAPI仕様ファイルはsrc/main/resources/swagger/api.ymlにあり、実装可能なエンドポイント・インタフェースを生成するために使用されます。
これらのインタフェースには、`501 Not implemented`HTTPステータスと空の本体で応答するデフォルトのメソッドがあります。
[swagger-editor](http://editor.swagger.io)などのツールを使用して定義を記述し、それを`src/main/resources/swagger/api.yml`に置き、次のコマンドを実行します。
```bash
./mvnw generate-sources
```
Or for gradle:
```bash
./gradlew openApiGenerate
```
次に、`${buildDirectory}/generated-sources/openapi/src/main/java/${package}/web/api/`で生成された"Delegate"インタフェースを`@Service`クラスで実装します。

有名な[petstore](http://petstore.swagger.io)についてコードを書く例は以下のとおりです。
```java
@Service
public class PetApiDelegateImpl implements PetApiDelegate {

    @Override
    public ResponseEntity<List<Pet>> findPetsByStatus(List<String> status) {
        return ResponseEntity.ok(
            status.stream()
                .distinct()
                .map(Pet.StatusEnum::fromValue)
                .map(statusEnum -> new Pet().id(RandomUtils.nextLong()).status(statusEnum))
                .collect(Collectors.toList())
        );
    }
}
```
デリゲートインタフェースに`NativeWebRequest`Beanを提供すると、オーバーライドされていないメソッドの基本的なサンプルボディが返されます（HTTPステータスコードは501のままです）。
これは、実際の実装を提供する前にエンドポイントをモックするのに便利です。
```java
@Service
public class PetApiDelegateImpl implements PetApiDelegate {

    private final NativeWebRequest request;

    public PetApiDelegateImpl(NativeWebRequest request) {
        this.request = request;
    }

    @Override
    public Optional<NativeWebRequest> getRequest() {
        return Optional.ofNullable(request);
    }
}
```
そうすれば、以下のような例を得ることができます。
```sh
$ curl -X GET --header 'Accept: application/json' 'http://localhost:8080/v2/pet/findByStatus?status=pending'
{  "photoUrls" : [ "photoUrls", "photoUrls" ],  "name" : "doggie",  "id" : 0,  "category" : {    "name" : "name",    "id" : 6  },  "tags" : [ {    "name" : "name",    "id" : 1  }, {    "name" : "name",    "id" : 1  } ],  "status" : "available"}%
$ curl -X GET --header 'Accept: application/xml' 'http://localhost:8080/v2/pet/findByStatus?status=pending'
<Pet>  <id>123456789</id>  <name>doggie</name>  <photoUrls>    <photoUrls>aeiou</photoUrls>  </photoUrls>  <tags>  </tags>  <status>aeiou</status></Pet>%
```

IDEがソースから出力フォルダを除外している可能性があります。生成されたクラスを検出するには、必ず構成を再ロードしてください。
これは、IDE UIまたはコマンドを使用して実行できます。

EclipseまたはVSCodeを使用する場合は以下のとおりです。

* mavenの場合
```bash
./mvnw eclipse:clean eclipse:eclipse
```
IntelliJを使う場合は以下となります。
* mavenの場合
```bash
./mvnw idea:idea
```

### `openapi-client`サブジェネレータの使用

JHipsterは、[Spring Cloud OpenFeign](https://docs.spring.io/spring-cloud-openfeign/docs/current/reference/html/)を使用したクライアントコードの生成や、OpenAPI/Swagger仕様を使用したリアクティブアプリ用のSpring Webclientのサポートも提供します。
生成されたクライアントは、モノリシックアプリケーションとマイクロサービスアプリケーションの両方で使用でき、Swagger v2とOpenAPI v3の定義をサポートします。このサブジェネレータを呼び出すには、`jhipster openapi-client`を実行してください。




