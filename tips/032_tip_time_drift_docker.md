---
layout: default
title: Dockerのタイムドリフト
sitemap:
priority: 0.1
lastmod: 2020-05-02T06:14:00-00:00
---

# Dockerのタイムドリフト

**このTipは[@SudharakaP](https://github.com/SudharakaP)によって提出されました**

Dockerを長時間（スリープサイクルを挟んで）実行する場合に考慮すべきことの1つは、
DockerコンテナとOSクロックの間にタイムドリフトが発生する場合があることです。

その結果、[https://github.com/jhipster/generator-jhipster/issues/11659](https://github.com/jhipster/generator-jhipster/issues/11659)のようなバグを見つけるのが難しくなります。

Dockerのタイムドリフトは、[Mac](https://github.com/docker/for-mac/issues/2076)と[Windows](https://github.com/docker/for-win/issues/4526)の両方で報告されており、
最も簡単な解決策は、長時間のスリープサイクルの後にDockerコンテナを再起動することです。