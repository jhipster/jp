import {
  SectionDescription,
  SectionTitle,
  SectionWrapper,
} from '@site/src/components/ui/SectionWrapper';
import EmbeddedVideo from '@site/src/components/EmbeddedVideo';
import styles from './styles.module.scss';

export default function Learn() {
  return (
    <SectionWrapper className={styles.section}>
      <SectionTitle>15分で JHipster を学びましょう</SectionTitle>

      <SectionDescription>
        <p>
          Matt Raible氏が、JHipster 8を使って
          Spring Boot + Angularアプリケーションを開発する方法を示すスクリーンキャストを作成しています。
        </p>
      </SectionDescription>

      <div className={styles.sectionVideo}>
        <EmbeddedVideo
          video="IfyjKCt6YHE"
          title="Get Started with JHipster 8"
        />
      </div>
    </SectionWrapper>
  );
}
