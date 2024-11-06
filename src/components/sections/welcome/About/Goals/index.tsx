import { RxStack } from 'react-icons/rx';
import { MdOutlineStyle } from 'react-icons/md';
import { GoWorkflow } from 'react-icons/go';
import { TbCloudDataConnection } from 'react-icons/tb';
import { GrDeploy } from 'react-icons/gr';

import {
  SectionDescription,
  SectionTitle,
} from '@site/src/components/ui/SectionWrapper';
import styles from './styles.module.scss';

export default function Goals() {
  return (
    <div className={styles.section}>
      <SectionTitle align="start">ゴール</SectionTitle>

      <SectionDescription align="start">
        <p>
          私たちのゴールは、完成されたモダンなWebアプリケーションやマイクロサービスのアーキテクチャを構成し、以下を統合することです：
        </p>
      </SectionDescription>

      <ul className={styles.sectionList}>
        <li>
          <div>
            <div className={styles.cardIcon}>
              <RxStack />
            </div>
            <h3 className={styles.cardTitle}>堅牢なサーバサイドのスタック</h3>
            <p className={styles.cardDescription}>
              優れたテストカバレッジがなされた、高性能で堅牢なサーバサイドのスタック
            </p>
          </div>
        </li>

        <li>
          <div>
            <div className={styles.cardIcon}>
              <MdOutlineStyle />
            </div>
            <h3 className={styles.cardTitle}>モダンで洗練されたUI</h3>
            <p className={styles.cardDescription}>
              Angular、React、Vueと、CSSにBootstrapを用いた、モバイルファーストな洗練されたモダンUI
            </p>
          </div>
        </li>

        <li>
          <div>
            <div className={styles.cardIcon}>
              <GoWorkflow />
            </div>
            <h3 className={styles.cardTitle}>パワフルなワークフロー</h3>
            <p className={styles.cardDescription}>
              WebpackやMaven/Gradleを用いてアプリケーションをビルドするパワフルなワークフロー
            </p>
          </div>
        </li>

        <li>
          <div>
            <div className={styles.cardIcon}>
              <TbCloudDataConnection />
            </div>
            <h3 className={styles.cardTitle}>弾性（Resilient）のあるアーキテクチャ</h3>
            <p className={styles.cardDescription}>
              クラウドネイティブの原則を意識した、弾性のあるマイクロサービスアーキテクチャ
            </p>
          </div>
        </li>

        <li>
          <div>
            <div className={styles.cardIcon}>
              <GrDeploy />
            </div>
            <h3 className={styles.cardTitle}>迅速なデプロイ</h3>
            <p className={styles.cardDescription}>
              Infrastructure as Codeにより迅速にクラウド☁️にデプロイ可能
            </p>
          </div>
        </li>
      </ul>
    </div>
  );
}
