import ContentMediaCard from '@site/src/components/ContentMediaCard';
import styles from './styles.module.scss';

export default function VideoTutorial() {
  return (
    <section>
      <div className={styles.sectionList}>
        <ContentMediaCard title="JHipsterによるブログアプリ開発のデモ" video="6lf64CctDAQ">
          <p>
            この15分間のチュートリアルでは、JHipster 7のアプリケーションを作成する方法、
            提供されているツールの使用方法、JDL Studioを使用して
            複数のエンティティとその関係を作成し、最終的な成果物を
            クラウドにデプロイする方法を紹介します。
          </p>
          <p>
            プレゼンター：Matt Raible (
            <a href="https://x.com/mraible">@mraible</a>)
          </p>
          <p>2021年4月30日公開</p>
        </ContentMediaCard>
      </div>

      <h2 className={styles.sectionTitle}>その他の最近のJHipsterの動画</h2>

      <div className={styles.sectionList}>
        <ContentMediaCard
          title="Javaによるマイクロサービスのためのマイクロフロントエンド"
          video="haTQ1xJKQQ8"
        >
          <p>
            <a href="https://x.com/mraible">Matt Raible</a>がマイクロフロントエンド
            とは何かを説明し、React、Spring
            Boot、JHipsterマイクロサービスでの使用方法を紹介します。
          </p>
          <p>
            2023年1月1日公開 |{' '}
            <a href="https://youtube.com/oktadev">OktaDev YouTube</a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard
          title="JHipster Liteとは？"
          video="RnLGnY-vzLI"
        >
          <p>
            <a href="https://x.com/juliendubois">Julien Dubois</a>が
            JHipsterとJHipster Liteを比較し、JHipster Liteの動作を紹介します。
          </p>
          <p>
            2022年10月14日公開 |{' '}
            <a href="https://www.youtube.com/@DevoxxForever">Devoxx YouTube</a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard
          title="Istioのサービスメッシュを用いたKubernetes上でのクラウドネイティブJavaマイクロサービスのビルドとデプロイ"
          video="NucXvPL1z5o"
        >
          <p>
            <a href="https://x.com/deepu105">Deepu K Sasidharan</a>が、
            Istio、Kubernetes、JHipster、Spring Cloudを使用して
            Javaマイクロサービスをクラウドにビルドおよびデプロイする方法を紹介します。
          </p>
          <p>
            2022年10月11日公開 |{' '}
            <a href="https://www.youtube.com/@DevoxxForever">Devoxx YouTube</a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard
          title="Spring SessionとRedisによるセキュアなアプリケーションのスケーリング"
          video="3kGrkVUZ_Fo"
        >
          <p>
            <a href="https://x.com/mraible">Matt Raible</a>が、
            Spring Sessionを使用してRedisにセッションを保存するSpring
            Bootアプリケーションの構成方法を紹介します。セッションは複数のノード間で共有され、
            ノード障害時にも保持されます。
          </p>
          <p>
            2022年4月5日公開 |{' '}
            <a href="https://youtube.com/oktadev">OktaDev YouTube</a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard
          title="React、Spring Boot、JHipsterを使ったフルスタックJava"
          video="PECnQs5bVbQ"
        >
          <p>
            <a href="https://x.com/mraible">Matt Raible</a>が、
            React、Spring Boot、JHipsterを使用して、洗練されたフルスタックのセキュアな
            Javaアプリケーションを作成する方法を紹介します。
          </p>
          <p>
            2022年1月26日公開 |{' '}
            <a href="https://youtube.com/oktadev">OktaDev YouTube</a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard
          title="Spring BootとJHipsterでKubernetesをクラウドへ"
          video="SQFl7ggNYIE"
        >
          <p>
            <a href="https://x.com/mraible">Matt Raible</a>が、
            Spring Cloud Gateway、Spring Boot、
            JHipsterを使用して開発されたマイクロサービスアーキテクチャをMinikubeと
            Google CloudにKubernetesでデプロイする方法を紹介します。
          </p>
          <p>
            2021年8月23日公開 |{' '}
            <a href="https://youtube.com/oktadev">OktaDev YouTube</a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard
          title="JHipsterでSpring BootとAngular 12のフルスタックアプリケーションを生成"
          video="V1g0aZtPAkw"
        >
          <p>
            <a href="https://x.com/bloch_gaetan">Gaëtan Bloch</a>が、
            JHipsterを使用してフルスタックアプリケーションを生成し、
            以下の機能を紹介します：テスト（JUnit、Jest、Testcontainersによる統合テスト、
            Cypressによるエンドツーエンドテスト、Gatlingによるパフォーマンステスト）、
            セキュリティ（JWT）、国際化、APIドキュメント化（OAS/Swagger）、品質保証
            （SonarQube、OWASP脆弱性チェック）、CI/CDパイプライン（GitHub
            Actions）およびHerokuへのクラウドデプロイ。
          </p>
          <p>
            2021年8月4日にライブ配信 |{' '}
            <a href="https://geekle.us/software_architecture">
              Geekle.us Worldwide Architecture Summit Vol.2
            </a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard
          title="Spring BootとJHipsterによるリアクティブなJavaマイクロサービスの構築"
          video="clkEUHWT9-M"
        >
          <p>
            <a href="https://x.com/mraible">Matt Raible</a>が、
            Spring BootとJHipsterを使ってリアクティブなマイクロサービスアーキテクチャを構築する方法を紹介します。
          </p>
          <p>
            2021年5月13日公開 |{' '}
            <a href="https://youtube.com/oktadev">OktaDev YouTube</a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard title="JHipsterの紹介" video="hfIIGc5lkME">
          <p>
            <a href="https://x.com/juliendubois">Julien Dubois</a>が
            <a href="https://www.dawsoncollege.qc.ca/dawscon/">DawsCon</a>で
            JHipsterを紹介しました。
          </p>
          <p>2021年1月15日にライブ配信</p>
        </ContentMediaCard>

        <ContentMediaCard
          title="JHipsterとKubernetesで自分の冒険を選ぼう"
          video="AG4z18qePEw"
        >
          <p>
            <a href="https://x.com/saturnism">Ray Tsang</a>と
            <a href="https://x.com/mraible">Matt Raible</a>が
            JHipsterでマイクロサービスアーキテクチャを構築し、Oktaの使用を設定し、
            Kubernetesでデプロイする方法を示します。
          </p>
          <p>
            2021年1月13日にライブ配信 |{' '}
            <a href="https://www.youtube.com/channel/UChJ6IHM_uy6dWLBiDAwYkpw">
            JChampions Conf YouTube
            </a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard
          title="JHipsterでセキュアなMicronautとAngularアプリを作る"
          video="zg2UtuD3-RE"
        >
          <p>
            <a href="https://x.com/mraible">Matt Raible</a>が、
            Java + JHipsterを使用してセキュアなMicronautとAngularのアプリを作成し、
            Herokuにデプロイする方法を紹介します。
          </p>
          <p>
            2020年9月17日公開 |{' '}
            <a href="https://youtube.com/oktadev">OktaDev YouTube</a>
          </p>
        </ContentMediaCard>

        <ContentMediaCard
          title="JHipsterをJWT認証からOAuth 2.0 / OIDC認証に10分で変更する"
          video="YIRjgd_3sMQ"
        >
          <p>
          <a href="https://x.com/mraible">@mraible</a>が、このスクリーンキャストで、
          JHipsterアプリの認証をJWTから
          OAuth 2.0 / OIDCに変更する方法を紹介しています。
          </p>
          <p>
            2019年9月20日公開 |{' '}
            <a href="https://youtube.com/oktadev">OktaDev YouTube</a>
          </p>
        </ContentMediaCard>
      </div>
    </section>
  );
}         
