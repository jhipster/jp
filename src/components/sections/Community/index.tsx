import { cva, type VariantProps } from 'class-variance-authority';
import clsx from 'clsx';

import {
  SectionDescription,
  SectionTitle,
  SectionWrapper,
} from '@site/src/components/ui/SectionWrapper';
import CommunityCard from './CommunityCard';
import GithubButton from '@site/src/components/GithubButton';
import styles from './styles.module.scss';

import { useCommunity } from './use-community';

const sectionVariants = cva(styles.section, {
  variants: {
    color: {
      default: styles.sectionDefault,
      light: styles.sectionLight,
    },
  },
  defaultVariants: {
    color: 'default',
  },
});

type Props = VariantProps<typeof sectionVariants>;

export default function Community({ color }: Props) {
  const { npmDownloads, githubConfig } = useCommunity();

  return (
    <SectionWrapper className={clsx(sectionVariants({ color }))}>
      <SectionTitle>コミュニティ</SectionTitle>

      <SectionDescription>
        <p>
          JHipsterはオープンソースであり、すべての開発はGitHubで行われています。
          JHipsterを支援したいとお考えの場合、スポンサーや支援者になることを検討してください。
          私たちとコーディングしたい場合は、お気軽にご参加ください！
          プロジェクトが気に入ったら、Githubで ⭐️ をお願いします。
        </p>
      </SectionDescription>

      <div className={styles.sectionList}>
          <CommunityCard
            value={`${npmDownloads.downloads}`}
            text="最近の30日間のダウンロード数"
          />
          <CommunityCard
            value={`${githubConfig.stargazers_count}`}
            text="GitHub スター数"
          />
          <CommunityCard value="600" text="コントリビューター数" postfix="+" />
      </div>

      <div className={styles.sectionButtons}>
        <GithubButton>GitHubで参加する</GithubButton>
      </div>
    </SectionWrapper>
  );
}
