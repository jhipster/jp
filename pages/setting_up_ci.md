---
layout: default
title: 継続的インテグレーションの設定
permalink: /setting-up-ci/
redirect_from:
  - /setting_up_ci.html
sitemap:
    priority: 0.7
    lastmod: 2018-08-03T14:40:00-00:00
---

# <i class="fa fa-stethoscope"></i> 継続的インテグレーションの設定

JHipsterアプリケーションの継続的インテグレーション（CI）のセットアップは、2つのソフトウェアスタックで構成されるビルドのメンテナンスに関連する複雑さのため、従来の一般的なSpring MVCアプリケーションよりも複雑です。

- MavenまたはGradleを使用したJavaバックエンドコード
- NodeJS、NPMを使用したJavaScriptフロントエンド

各スタックには、解決すべき潜在的な競合を持つ独自の依存関係管理（Mavenアーティファクト、NPMパッケージ）が付属しています。

JHipsterは、次のCIシステムをサポートします。

- Jenkins
    - [Jenkinsのセットアップ1]({{ site.url }}/setting-up-ci-jenkins1/)
    - [Jenkinsのセットアップ2]({{ site.url }}/setting-up-ci-jenkins2/) （推奨）
- Travis:[Travisドキュメント](https://docs.travis-ci.com/user/getting-started/)を参照してください
- GitLab CI:[GitLab CIドキュメント](https://about.gitlab.com/gitlab-ci/)を参照してください
- Azure Pipelines:[Azure Pipelinesドキュメント](https://docs.microsoft.com/fr-fr/azure/devops/pipelines/?view=vsts)を参照してください
- GitHub Actions:[GitHub Actionsドキュメント](https://github.com/features/actions)を参照してください
- CircleCI:[CircleCIドキュメント](https://circleci.com/docs/)

## サブジェネレータの実行

これらの構成ファイルを生成するには、プロジェクトフォルダで次のコマンドを実行します。

`jhipster ci-cd`

次に、すべての質問に答えます。


### どのCI/CDパイプラインを生成しますか?

生成できるCI/CDパイプラインは以下です。

- Jenkins pipeline
- Azure Pipelines
- GitLab CI
- GitHub Actions
- Travis CI
- CircleCI

**注**: Jenkins pipelineを選択すると、新しい`src/main/docker/jenkins.yml`ファイルが生成されます。
そのため、次のコマンドを実行することで、Jenkinsをローカルでテストできます。

```
docker-compose -f src/main/docker/jenkins.yml up -d
```

### Dockerコンテナでビルドを実行しますか?(Jenkins/GitLab)

Dockerがインストールされている場合は、Dockerコンテナ内でビルドを実行できます。

### GitLab CIで、Dockerコンテナ(ヒント:GitLab.comはDockerコンテナを使用)でビルドを実行しますか?(GitLab)

プライベートGitLab CIを使用する場合は、ランナーを直接使用できます。

公式のGitLab.comパイプラインを使用する場合は、Dockerコンテナを使用する必要があります。

### ビルドステータスをGitLabに送信しますか?(Jenkins)

JenkinsがGitLabリポジトリに依存している場合は、ビルドステータスをGitLabに送信できます。なおJenkinsは正しく設定されている必要があります。

### どのタスク/統合を含めますか?

- アプリケーションを*Artifactory*にデプロイ
- *Sonar*でコードを解析
- *Docker*イメージの構築と公開
- *Snyk*：セキュリティ脆弱性の依存性スキャン（SNYK_TOKENが必要）
- *Heroku*にデプロイ（CIサービスでHEROKU_API_KEYが設定されている必要があります）
- Cypressダッシュボードを有効にしますか（CIサービスでCYPRESS_PROJECT_IDとCYPRESS_RECORD_KEYの両方が設定されている必要があります）

### アプリケーションを*Artifactory*にデプロイする (Jenkins/GitLab)

- *Artifactory*：スナップショットのdistributionManagementのIDは何ですか？
- *Artifactory*：スナップショットのdistributionManagementのURLは何ですか？
- *Artifactory*：リリースのdistributionManagementのIDは何ですか？
- *Artifactory*：リリースのdistributionManagementのURLは何ですか？

### *Sonar*を使用してコードを分析

- *Sonar*：Sonarサーバの名前は何ですか？

Jenkins Configurationで定義されているSonarサーバの名前を選択します。

- *Sonar*：SonarサーバのURLは何ですか？
- *Sonar*：Sonarサーバの組織は何ですか？

ここで、Sonar Analyzeを[SonarCloud.io](https://sonarcloud.io)にプッシュすることを選択できます。
この場合は、`SONAR_TOKEN`環境変数を追加する必要があります。

### *Docker*イメージのビルドと公開

- *Docker*：DockerレジストリのURLは何ですか？

デフォルトでは、Docker Hub（[https://registry.hub.docker.com](https://registry.hub.docker.com)）を使用できます。

- *Docker*：DockerレジストリのJenkins Credentials IDは何ですか？

デフォルトでは、`docker login`を使用できます。

- *Docker*：Dockerレジストリの組織名は何ですか？

### Snyk：セキュリティの脆弱性に対する依存性スキャン

`SNYK_TOKEN`環境変数を追加する必要があります（[Snykアカウント](https://app.snyk.io/account)を確認してください）

詳細なドキュメントは[https://snyk.io/](https://snyk.io/)にあります。

### Cypress Dashboard：Cypressが提供するWebアプリケーション内でテストを記録

`CYPRESS_PROJECT_ID`と`CYPRESS_RECORD_KEY`環境変数を追加する必要があります（[ダッシュボードプロジェクト](https://dashboard.cypress.io/)を確認してください）。

このレコードを無効にするには、`CYPRESS_ENABLE_RECORD`環境変数の値をfalseに変更します。

ドキュメントの詳細については、[cypress.io/dashboard](https://www.cypress.io/dashboard/)を参照してください。

### *Heroku*にデプロイ

- *Heroku*：Herokuアプリケーションの名前はなんですか？

`HEROKU_API_KEY`環境変数を追加する必要があります。

注：Herokuへのデプロイメントを使用する前に、[Herokuサブジェネレータ]({{ site.url }}/heroku)をローカルで使用する必要があります。
継続的インテグレーション・ツールに必要なすべてのファイルが作成されます。


## 追加情報

OSやプロジェクトをプッシュした場所によっては、CI/CDを使用する前にラッパーを実行可能にする必要があります。

Mavenを使用する場合は以下です。

- `chmod +x mvnw`
- `git update-index --chmod=+x mvnw`

Gradleを使用する場合は以下です。

- `chmod +x gradlew`
- `git update-index --chmod=+x gradlew`


## 環境変数に関するドキュメント

- Jenkins pipeline：[Credentials plugin](https://wiki.jenkins-ci.org/display/JENKINS/Credentials+Plugin)を使用します。
- GitLab CI：[secret-variablesに関するドキュメント](https://docs.gitlab.com/ce/ci/variables/#secret-variables)を参照ください。
- Travis CI：[環境変数](https://docs.travis-ci.com/user/environment-variables/)を参照ください。
- GitHub Actions：[環境変数に関するドキュメント](https://help.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables)を参照ください。
- Azure Pipelines：[定義済み変数に関するドキュメント](https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&tabs=yaml)を参照ください。
- CircleCI：[環境変数に関するドキュメント](https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables)を参照ください。
