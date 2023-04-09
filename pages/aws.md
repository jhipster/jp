---
layout: default
title: AWSへのデプロイ
permalink: /aws/
# redirect_from:
#   - /aws.html
sitemap:
    priority: 0.7
    lastmod: 2018-01-17T00:00:00-00:00
---

# <i class="fa fa-cloud-upload"></i> Deploying to AWS

[![Powered by AWS Cloud Computing]({{ site.url }}/images/logo/logo-aws.png)](https://aws.amazon.com/what-is-cloud-computing)

## *aws*サブジェネレータ

このサブジェネレータを使用すると、インフラストラクチャのプロビジョニングに[AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)を使用して、JHipsterアプリケーションを[Amazon AWSクラウド](https://aws.amazon.com/)に自動的にデプロイできます。

<div class="alert alert-info"> <i>ヒント:</i>Elastic Beanstalkの代わりに、<a href="{{ site.url }}/cloudcaptain/">CloudCaptain</a>を使ってJHipsterアプリケーションをデプロイすることもできます。
CloudCaptainは、JHipsterの優れたサポートに加えて、MySQLおよびPostgreSQLデータベースの両方をサポートしています。</div>

### 制限事項

*   SQLデータベースでのみ使用できます（ただし、OracleおよびMicrosoft SQL Serverはサポートされていません）。
*   WebSocketは、デフォルトではロードバランサの背後で動作しません。

### 前提条件

サブジェネレータを実行する前に、AWS SDKの認証情報を作成して、JHipsterがElastic Beanstalkにデプロイできるようにします。

Amazon AWSアカウントにログインし、プログラムによるアクセス権を持つIAMユーザーを作成します。

次のポリシーをアタッチして、ユーザに必要な権限を付与します。
- `AdministratorAccess-AWSElasticBeanstalk`
- `AmazonS3FullAccess`
- `AmazonRDSFullAccess`
- `IAMFullAccess`

ユーザーを作成し、新しい認証情報が含まれた`csv`ファイルをダウンロードします。これらを使用して、次のように、Mac/Linuxでは`~/.aws/credentials`、Windowsでは`C:\Users\USERNAME\.aws\credentials`という認証情報ファイルを作成します。
```ini
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
```
すでに`default`プロファイルがある場合は、新しい名前付きプロファイルを作成し、環境変数`AWS_PROFILE`に新しいプロファイル名を設定します（詳細は[ここ](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)を参照してください）。

`aws sts get-caller-identity`を実行して、アクセスをテストします。

### アプリケーションのデプロイ

アプリケーションをAmazon AWSにデプロイするには、次のように入力します。

`jhipster aws`

次のプロンプトが表示されます。
- Application name：アプリケーションを構成するElastic Beanstalkコンポーネントのコレクションの名前（デフォルトはプロジェクト名）
- Environment name：アプリケーションを実行するAWSリソース環境の名前
- Name of S3 bucket：静的Webコンポーネントを保持します
- Database name：RDSデータベースの名前
- Database username：RDSデータベースユーザ名
- Database password：[hidden]
- On which EC2 instance type do you want to deploy?（どのEC2インスタンスタイプにデプロイしますか？）：AWS EC2仮想マシンの容量を選択します
- On which RDS instance class do you want to deploy（どのRDSインスタンスクラスに展開しますか？）：RDSデータベースインスタンスの容量を選択します
- On which region do you want to deploy?（どのリージョンにデプロイしますか？）：インスタンスをホストするAWSリージョンを選択します

これにより、アプリケーションが「プロダクション」モードでパッケージ化され、（SQLデータベースを使用して）Beanstalkアプリケーションが作成され、S3にコードがアップロードされ、アプリケーションが起動されます。

### 展開したアプリケーションの更新

`jhipster aws`を使用してサブジェネレータを再度実行することで、デプロイされたアプリケーションを更新できます。

データベースの資格情報の入力が再度求められますが、更新時には無視されます。

### アプリケーションの削除

- Elastic Beanstalkを削除します。
- アプリケーションに関連するS3バケットを削除します。
- [Amazon Relational Database Service(RDS)](https://aws.amazon.com/rds/)インスタンスを削除します。
- アプリケーションに関連するEC2セキュリティグループを削除します。
これには`Enable database access to Beanstalk application`と書かれているはずです。

### 詳細情報

*   [JavaScript用のAWS SDK](http://aws.amazon.com/sdk-for-node-js)
*   [WARアップロードの進行状況バー](https://github.com/tj/node-progress)
