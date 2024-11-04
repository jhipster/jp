import {
  SectionDescription,
  SectionTitle,
  SectionWrapper,
} from '@site/src/components/ui/SectionWrapper';
import GithubButton from '@site/src/components/GithubButton';
import styles from './styles.module.scss';

export default function ConnectCommunity() {
  return (
    <SectionWrapper>
      <div className={styles.sectionContent}>
        <div>
          <SectionTitle className={styles.sectionTitle} align="start">
            コミュニティとつながる
          </SectionTitle>

          <SectionDescription
            className={styles.sectionDescription}
            align="start"
          >
            <p>
              気軽に質問したり、問題を報告したり、貢献したり、新しい人々と出会いましょう
            </p>
          </SectionDescription>
        </div>

        <GithubButton>GitHubで参加する</GithubButton>
      </div>
    </SectionWrapper>
  );
}
