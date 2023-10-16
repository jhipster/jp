---
layout: default
title: Microsoft Azureへのデプロイ
permalink: /azure/
sitemap:
    priority: 0.7
    lastmod: 2018-08-24T00:00:00-00:00
---

# <i class="fa fa-cloud-upload"></i> Microsoft Azureへのデプロイ

[Microsoft Azure](https://azure.microsoft.com/overview/?WT.mc_id=online-jhipster-judubois)は、クラウドでJHipsterアプリケーションを実行するための優れたソリューションです。

- 最も簡単な方法は、[JHipster Azure Spring Apps](https://github.com/Azure/generator-jhipster-azure-spring-apps)を使用して、プロジェクトをエンドツーエンドで作成してデプロイすることです。 JHipster Azure Spring Appsは、フルスタックのSpringアプリケーション開発を合理化するように設計されており、Azure Spring Appsの堅牢なインフラストラクチャを活用して、これまでにない容易さと効率性でプロジェクトを実現します。
(https://azure.microsoft.com/services/spring-apps/?WT.mc_id=online-jhipster-judubois)
- Spring Bootマイクロサービスを使用している場合、[Azure Spring Apps]はJHipsterアプリケーションを完全にサポートします。[Quickstart](https://learn.microsoft.com/azure/spring-apps/quickstart-deploy-microservice-apps)で詳細を読むことができます。
- また、[Azure App Service](https://azure.microsoft.com/services/app-service/?WT.mc_id=online-jhipster-judubois)を使ってモノリスをデプロイすることもできます。
- 他のDockerおよびKubernetesクラウドプロバイダと同様に、JHipster DockerおよびKubernetesサポートを使用して、DockerイメージをMicrosoft Azureにデプロイできます。これらのオプションの詳細については、[Docker Composeドキュメント]({{ site.url }}/docker-compose/)および[Kubernetesドキュメント]({{ site.url }}/kubernetes/)に従ってください。

[![Microsoft Azure]({{ site.url }}/images/logo/logo-azure.png)](https://azure.microsoft.com/overview/?WT.mc_id=online-jhipster-judubois)

<h2>NubesGenを使用したデプロイ</h2>

[NubesGen](https://www.nubesgen.com)はJHipsterアプリケーションを完全にサポートするデプロイメントプラットフォームであり、アプリケーションをAzureにデプロイするための最良のソリューションです。

NubesGenを使用してJHipsterアプリケーションをデプロイするには、ドロップダウン・メニューから次の項目を選択します。

- "Spring Boot (Java) with Maven"で、MavenでJHipsterアプリケーションを実行します。
- "Spring Boot (Java) with Gradle"で、GradleでJHipsterアプリケーションを実行します。
- "Docker with Spring Boot"で、JHipsterアプリケーションをDockerでパッケージ化し、Dockerで実行します。パフォーマンスはMavenやGradleよりも優れているかもしれませんが、監視オプションが少なく、MicrosoftからのJavaサポートもありません。

[NubesGenのWebサイト](https://www.nubesgen.com)にアクセスすると、完全なドキュメントが表示されます。

<h2>[非推奨] "azure"サブジェネレータを使用したデプロイ</h2>

JHipsterには、以前のバージョンで文書化されている"azure"サブジェネレータがまだありますが、非推奨になりました。
