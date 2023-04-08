---
layout: default
title: Jenkins 1のセットアップ
permalink: /setting-up-ci-jenkins1/
sitemap:
    priority: 0.7
    lastmod: 2016-11-03T12:40:00-00:00
---

# <i class="fa fa-wrench"></i> Jenkinsサーバの設定

JHipster用にJenkinsサーバを設定するには、次のガイドを参照してください。

- [LinuxでのJenkins 1のセットアップ]({{ site.url }}/setting-up-ci-linux/)
- [WindowsでのJenkins 1のセットアップ]({{ site.url }}/setting-up-ci-windows/)

#<i class="fa fa-sliders"></i> Jenkinsの設定

JenkinsでJHipsterプロジェクトを設定するには、次の設定を使用します。

## Mavenの場合:

```
* Project name: `yourApplicationName`
* Source Code Management
    * Git Repository: `git@github.com:xxxx/yourApplicationName.git`
    * Branches to build: `*/main`
    * Additional Behaviours: `Wipe out repository & force clone`
* Build Triggers
    * Poll SCM / Schedule: `H/5 * * * *`
* Build<% if (buildTool == 'maven') { %>
    * Invoke Maven / Tasks: `-Pprod clean package`
    * Execute Shell / Command:
        ````
        mvn spring-boot:run &
        bootPid=$!
        sleep 30s
        gulp itest
        kill $bootPid
        ````
* Post-build Actions
    * Publish JUnit test result report / Test Report XMLs: `build/test-results/*.xml`
```

## Gradleの場合:
```
* Project name: `yourApplicationName`
* Source Code Management
    * Git Repository: `git@github.com:xxxx/yourApplicationName.git`
    * Branches to build: `*/main`
    * Additional Behaviours: `Wipe out repository & force clone`
* Build Triggers
    * Poll SCM / Schedule: `H/5 * * * *`
* Build
    * Invoke Gradle script / Use Gradle Wrapper / Tasks: `-Pprod clean test bootWar`
    * Execute Shell / Command:
        ````
        ./gradlew bootRun &
        bootPid=$!
        sleep 30s
        gulp itest
        kill $bootPid
        ````
* Post-build Actions
    * Publish JUnit test result report / Test Report XMLs: `build/test-results/*.xml`
```

