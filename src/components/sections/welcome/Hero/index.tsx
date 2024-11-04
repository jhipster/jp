import Link from '@docusaurus/Link';
import clsx from 'clsx';

import GithubButton from '@site/src/components/GithubButton';
import HeroFamily from '@site/static/images/logo/hero-family.svg';
import styles from './styles.module.scss';

export default function Hero() {
  return (
    <header className={styles.section}>
      <div className={clsx('container', styles.sectionContent)}>
        <div>
          <h1 className={styles.sectionTitle}>
            <br /> Java <span className="text--primary">Hipster</span>の皆さん<br />
            こんにちは!
          </h1>

          <p className={styles.sectionDescription}>
            JHipsterはモダンなWebアプリケーションやマイクロサービスの<br />
            アーキテクチャを素早く生成、開発、デプロイできる<br />
            開発プラットフォームです。
          </p>

          <div className={styles.sectionButtons}>
            <Link className="button button--primary" to="/getting-started">
              始める
            </Link>
            <GithubButton>GitHub</GithubButton>
          </div>
        </div>

        <HeroFamily className={styles.sectionImage} />
      </div>
    </header>
  );
}
