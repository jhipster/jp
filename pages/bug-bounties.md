---
layout: default
title: バグ報奨金
permalink: /bug-bounties/
sitemap:
    priority: 0.1
    lastmod: 2018-07-20T00:00:00-00:00
---
# <i class="fa fa-usd"></i> バグ報奨金

## はじめに

[JHipsterバグ追跡システム](https://github.com/jhipster/generator-jhipster/issues)で開かれたチケットには、"\$\$ bug-bounty \$\$"というラベルを付けることができます。チケットを解決した人には、チケットに応じて100ドル、200ドル、300ドル、500ドルのいずれかの金額が与えられます。

## バグ報奨金は誰が作れますか?

<<<<<<< HEAD
- [シルバー、ゴールド、プラチナスポンサー]({{ site.url }}/sponsors/)
- 3人の[コアチームプロジェクトリーダー]({{ site.url }}/team/)、[@jdubois](https://github.com/jdubois)、[@deepu105](https://github.com/deepu105)、[@pascalgrimaud](https://github.com/pascalgrimaud)
=======
- [Silver, gold and platinum sponsors]({{ site.url }}/sponsors/)
- The [project leads]({{ site.url }}/team/#project-leads) and [governing body]({{ site.url }}/team/#governing-body).
>>>>>>> upstream/main

## バグ報奨金はいくらですか?

"\$\$ bug-bounty \$\$"ラベルの隣には、"$100"、"$200"、"$300"、または"$500"ラベルが表示され、バグ報奨金の価値が示されます。

## 現在オープンされているバグ報奨金のリストはどこにありますか?

バグ報奨金は、主にメインプロジェクトで利用できますが、GitHubのJHipster組織のサブプロジェクトで開くこともできます。

- [すべてのプロジェクトのオープンなバグ報奨金](https://github.com/search?l=&p=1&q=is%3Aissue+is%3Aopen+label%3A%22%24%24+bug-bounty+%24%24%22+user%3Ajhipster+state%3Aopen&ref=advsearch&type=Issues&utf8=%E2%9C%93)
- [メインプロジェクトのオープンなバグ報奨金](https://github.com/jhipster/generator-jhipster/labels/%24%24%20bug-bounty%20%24%24)
- [JHipster VueJSサブプロジェクトのオープンなバグ報奨金](https://github.com/jhipster/jhipster-vuejs/labels/%24%24%20bug-bounty%20%24%24)

楽しいバグ探しを(^_^)

## バグ報奨金の仕組み

チケットが作成されると、次の2つのアクションによってバグ報奨金ラベルを取得できます。

<<<<<<< HEAD
- シルバーまたはゴールドのスポンサーが、バグ報奨金ラベルの追加を求めるコメントを追加し、[@jdubois](https://github.com/jdubois)、[@deepu105](https://github.com/deepu105)または[@pascalgrimaud](https://github.com/pascalgrimaud)にメンションします。
- [@jdubois](https://github.com/jdubois)、[@deepu105](https://github.com/deepu105)または[@pascalgrimaud](https://github.com/pascalgrimaud)がバグ報奨金ラベルを直接追加します。これは、重要な新機能、重大なバグ、長期にわたる問題、あるいは時間のかかるタスクであると考えられるためです。問題に取り組んでいて、それが報奨金に値すると考える場合は、プロジェクトリーダーの1人に尋ねることをためらわないでください。

バグ報奨金を有効にするには、
[@jdubois](https://github.com/jdubois)、[@deepu105](https://github.com/deepu105)または[@pascalgrimaud](https://github.com/pascalgrimaud)のいずれかが[\$\$ bug-bounty \$\$](https://github.com/jhipster/generator-jhipster/labels/%24%24%20bug-bounty%20%24%24)ラベルを追加する必要があります。また、"$100"、"$200"、"$300"、または"$500"のラベルを付けて、そのタグの価値を示す必要がありますが、そのタグを忘れた場合は、デフォルトで"$100"の価値があります。
=======
- a silver or gold sponsor adds a comment asking to add the bug bounty label and mentioning one of the [project leads]({{ site.url }}/team/#project-leads) on GitHub.
- [project leads]({{ site.url }}/team/#project-leads) and [governing body]({{ site.url }}/team/#governing-body) directly add the bug bounty label, as they believe it is an important new feature, a critical bug, a long-standing issue, or a time-consuming task. If you are working on an issue and if you think it deserves a bounty don't hesitate to ask one of the project leads.

To be valid, the bug bounty should then have the [\$\$ bug-bounty \$\$](https://github.com/jhipster/generator-jhipster/labels/%24%24%20bug-bounty%20%24%24) label added by either
[project leads]({{ site.url }}/team/#project-leads) or [governing body]({{ site.url }}/team/#governing-body). It should also have a "$100", "$200", "$300" or "$500" label to tell how much it is worth, but if that tag has been forgotten, it is by default worth "$100".
>>>>>>> upstream/main

## 報奨金を得る方法

<<<<<<< HEAD
バグ報奨金が作られれば、誰でも修正を提案できます（[@jdubois](https://github.com/jdubois)、[@deepu105](https://github.com/deepu105)や[@pascalgrimaud](https://github.com/pascalgrimaud)でさえも!）。私たちの目標は、そのお金を使って、何かができるだけ早く修正されるようにすることです。
=======
Once a bug bounty is created, anybody can propose a fix (even the [project leads]({{ site.url }}/team/#project-leads) and [governing body]({{ site.url }}/team/#governing-body)!). Our goal is to spend that money so that something is fixed as quickly as possible.
>>>>>>> upstream/main

金銭を請求するには、次の条件を満たす必要があります。

<<<<<<< HEAD
- "\$\$ bug-bounty \$\$"ラベルの付いたチケットを修正するプルリクエストを作成します。
- チケットを自動的に閉じるには、`Fix`キーワードを含むコミットメッセージが1つ必要です。たとえば、チケット`#1234`を閉じるには、`Fix #1234`と指定します。
- そのプルリクエストは、コアチームの誰かによってマージされる必要があります。複数のプルリクエストがある場合、コアチームメンバーは最新のプルリクエストまたは最適なプルリクエストを選択します。これは、チームメンバーがプロジェクトに最適なプルリクエストを決定するためです。
- その後、[JHipster OpenCollectiveに100ドル、200ドル、300ドル、または500ドルの費用を追加](https://opencollective.com/generator-jhipster/expenses/new)できます。説明にプルリクエストへのリンクを追加する必要があります（例：`$100 bug bounty claim for https://github.com/jhipster/generator-jhipster/pull/1234`）。
- 次に、Pull Requestにコメントを追加する必要があります。このコメントには、OpenCollective費用へのリンクとともに、お金を請求したことを示します。これにより、問題を修正してお金を請求したのが同じ人物であることが確認されます。
- その費用は[@jdubois](https://github.com/jdubois)、[@deepu105](https://github.com/deepu105)または[@pascalgrimaud](https://github.com/pascalgrimaud)によって検証され、あなたのペイパルアカウントでお金を受け取ることになります。
=======
- Create a Pull Request that fixes a ticket with the "\$\$ bug-bounty \$\$" label.
- In order to close the ticket automatically, you must have one commit message with the `Fix` keyword. For example, `Fix #1234` to close ticket `#1234`.
- That Pull Request must be merged by someone from the core team. If there are several Pull Requests, the core team member either selects the most recent one or the best one - that's up to the team member to decide what is best for the project.
- You can then [add a $100, $200, $300 or $500 expense on the JHipster OpenCollective](https://opencollective.com/generator-jhipster/expenses/new). You must add a link to your Pull Request in the description (for example: `$100 bug bounty claim for https://github.com/jhipster/generator-jhipster/pull/1234`).
- Then, you must add a comment on your Pull Request, telling that you claimed the money, with a link to your OpenCollective expense. This is to be sure it is the same person who fixed the issue and claimed the money.
- That expense will then be validated by the [project leads]({{ site.url }}/team/#project-leads) or [governing body]({{ site.url }}/team/#governing-body), and you will receive your money on your Paypal account.
>>>>>>> upstream/main
