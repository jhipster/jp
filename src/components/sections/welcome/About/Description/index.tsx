import styles from './styles.module.scss';

export default function Description() {
  return (
    <ul className={styles.section}>
      <li>
        JHipsterは、モダンなWebアプリケーションやマイクロサービスのアーキテクチャを迅速に生成、
        開発、デプロイできる開発プラットフォームです。
      </li>
      <li>
        Angular, React, Vueなど、多くのフロントエンド技術をサポートしています。
        IonicやReact Nativeなどのモバイルアプリもサポートしています！
      </li>
      <li>
        バックエンドでは、Spring Boot (JavaまたはKotlin), Micronaut, Quarkus, Node.js,
        .NETをサポートとしています。
      </li>
      <li>
        デプロイにおいては、DockerやKubernetesによるクラウドネイティブの原則を採用しています。
      </li>
      <li>
        デプロイ支援としてAWS, Azure, Google Cloud Platform, Heroku, and OpenShiftに対応しています。
      </li>
    </ul>
  );
}
