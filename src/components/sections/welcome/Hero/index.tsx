import Link from '@docusaurus/Link';
import clsx from 'clsx';

import GithubButton from '@site/src/components/GithubButton';
import styles from './styles.module.scss';

const heroImageSrc =
  require('@site/static/images/logo/hero-family.webp').default;

export default function Hero() {
  return (
    <>
      <link rel="preload" as="image" href={heroImageSrc} />

      <header className={styles.section}>
        <div className={clsx('container', styles.sectionContent)}>
          <div>
            <h1 className={styles.sectionTitle}>
              <br /> Java <span className="text--primary">Hipster</span>の皆さん<br />
              こんにちは!
            </h1>

            <p className={styles.sectionDescription}>
              JHipsterはモダンなWebアプリケーションやマイクロサービスの<br />
              アーキテクチャを素早く生成、開発、デプロイできる<br />開発プラットフォームです。
            </p>

            <div className={styles.sectionButtons}>
              <Link className="button button--primary" to="/getting-started">
                始める
              </Link>
              <GithubButton>GitHub</GithubButton>
            </div>
          </div>

          <img
            className={styles.sectionImage}
            src={heroImageSrc}
            alt="JHipster family"
            width={476}
            height={380}
          />
        </div>
      </header>
    </>
  );
}
