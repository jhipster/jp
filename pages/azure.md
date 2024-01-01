---
layout: default
title: Microsoft Azureへのデプロイ
permalink: /azure/
sitemap:
    priority: 0.7
    lastmod: 2023-12-19T00:00:00-00:00
---

# <i class="fa fa-cloud-upload"></i> Microsoft Azureへのデプロイ

[Microsoft Azure](https://azure.microsoft.com/overview/?WT.mc_id=online-jhipster-judubois)は、クラウドでJHipsterアプリケーションを実行するための優れたソリューションです。

- 最も簡単な方法は、[JHipster Azure Spring Apps](https://github.com/Azure/generator-jhipster-azure-spring-apps)を使用して、プロジェクトをエンドツーエンドで作成してデプロイすることです。 JHipster Azure Spring Appsは、フルスタックのSpringアプリケーション開発を合理化するように設計されており、Azure Spring Appsの堅牢なインフラストラクチャを活用して、これまでにない容易さと効率性でプロジェクトを実現します。
- Spring Bootマイクロサービスを使用している場合、[Azure Spring Apps](https://azure.microsoft.com/services/spring-apps/?WT.mc_id=online-jhipster-judubois) はJHipsterアプリケーションを完全にサポートします。[Quickstart](https://learn.microsoft.com/azure/spring-apps/quickstart-deploy-microservice-apps)で詳細を読むことができます。
- また、[Azure App Service](https://azure.microsoft.com/services/app-service/?WT.mc_id=online-jhipster-judubois)を使ってモノリスをデプロイすることもできます。
- 他のDockerおよびKubernetesクラウドプロバイダと同様に、JHipster DockerおよびKubernetesサポートを使用して、DockerイメージをMicrosoft Azureにデプロイできます。これらのオプションの詳細については、[Docker Composeドキュメント]({{ site.url }}/docker-compose/)および[Kubernetesドキュメント]({{ site.url }}/kubernetes/)に従ってください。

[![Microsoft Azure]({{ site.url }}/images/logo/logo-azure.png)](https://azure.microsoft.com/overview/?WT.mc_id=java-0000-judubois)

<h2>NubesGenを使用したデプロイ</h2>

[NubesGen](https://www.nubesgen.com)はJHipsterアプリケーションを完全にサポートするデプロイメントプラットフォームであり、アプリケーションをAzureにデプロイするための最良のソリューションです。

NubesGenを使用してJHipsterアプリケーションをデプロイするには、ドロップダウン・メニューから次の項目を選択します。

- "Spring Boot (Java) with Maven"で、MavenでJHipsterアプリケーションを実行します。
- "Spring Boot (Java) with Gradle"で、GradleでJHipsterアプリケーションを実行します。
- "Docker with Spring Boot"で、JHipsterアプリケーションをDockerでパッケージ化し、Dockerで実行します。パフォーマンスはMavenやGradleよりも優れているかもしれませんが、監視オプションが少なく、MicrosoftからのJavaサポートもありません。

[NubesGenのWebサイト](https://www.nubesgen.com)にアクセスすると、完全なドキュメントが表示されます。

## start.jhipster.techで生成されたazdを使用したデプロイ

[start.jhipster.tech/generate-azure-application](https://start.jhipster.tech/generate-azure-application)経由で、Azure Spring Appsへの組み込みのazdデプロイメントを備えた、新しいJHipsterアプリケーションの作成もできます。デプロイメントテンプレートの恩恵により、`azd up` という1つの簡単なコマンドでデプロイできるオープンソースのツールキット Azure Development CLI を活用します。

<div class="thumbnail no-margin-bottom">
    <div class="video-container">
        <iframe width="420" height="315" src="https://www.youtube.com/embed/AmxPv_5Bs_k?si=HeDmf113Uld0bCbS&amp;start=33" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    </div>
    <div class="caption">
        <h3 id="thumbnail-label">Azure Spring Apps の JHipster デモ<a class="anchorjs-link" href="#thumbnail-label"><span class="anchorjs-icon"></span></a></h3>
        <p>この4分間のチュートリアルでは、 [start.jhipster.tech/generate-azure-application](https://start.jhipster.tech/generate-azure-application) を介し、Azure Spring Appsへの組み込みのazdデプロイメントを使用してJHipsterアプリケーションを生成する方法を説明します。</p>
        <p>プレゼンター Sandra Ahlgrimm (<a href="https://twitter.com/skriemhild">@skriemhild</a>)</p>
        <p>2023年9月26日 公開</p>
    </div>
</div>
<<<<<<< HEAD

## [非推奨] "azure"サブジェネレータを使用したデプロイ

JHipsterには、以前のバージョンで文書化されている"azure"サブジェネレータがまだありますが、非推奨になりました。
=======
>>>>>>> upstream/main
