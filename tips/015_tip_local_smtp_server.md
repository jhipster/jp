---
layout: default
title: ローカルSMTPサーバ
sitemap:
priority: 0.5
lastmod: 2016-05-21T22:22:00-00:00
---

# ローカルSMTPサーバ

__このTipは[@pascalgrimaud](https://github.com/pascalgrimaud)から提出されました__

**警告!** このヒントは、JHipsterが直接サポートしていない別のプロジェクトに依存しています。

プロジェクト[djfarrelly/maildev](https://github.com/djfarrelly/MailDev)は、プロジェクトの開発中に生成された電子メールをテストするための簡単な方法で、使いやすいWebインタフェースを備えています。

Dockerを使用してSMTPサーバをローカルで起動するには、次の手順を実行します。

```
docker container run -d -p 1080:80 -p 25:25 djfarrelly/maildev
```
