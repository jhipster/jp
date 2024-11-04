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
<<<<<<< HEAD
          JHipsterはオープンソースであり、すべての開発はGitHubで行われています。
          JHipsterを支援したいとお考えの場合、スポンサーや支援者になることを検討してください。
          私たちとコーディングしたい場合は、お気軽にご参加ください！
          プロジェクトが気に入ったら、Githubで ⭐️ をお願いします。
        </p>
      </SectionDescription>

      <ul className={styles.sectionList}>
        <li>
          <CommunityCard
            value={`${npmDownloads.downloads}`}
            text="最近の30日間のダウンロード数"
          />
        </li>
        <li>
          <CommunityCard
            value={`${githubConfig.stargazers_count}`}
            text="GitHub スター数"
          />
        </li>
        <li>
          <CommunityCard value="600" text="コントリビューター数" postfix="+" />
        </li>
      </ul>
=======
          JHipster is Open Source, and all development is done on GitHub. If you
          use JHipster, consider becoming a sponsor or a backer. If you want to
          code with us, feel free to join! If you like the project, please give
          us a ⭐️ on GitHub.
        </p>
      </SectionDescription>

      <div className={styles.sectionList}>
        <CommunityCard
          value={`${npmDownloads.downloads}`}
          text="Downloads in last 30 days"
        />
        <CommunityCard
          value={`${githubConfig.stargazers_count}`}
          text="GitHub Stars"
        />
        <CommunityCard value="600" text="Contributors" postfix="+" />
      </div>
>>>>>>> upstream/main

      <div className={styles.sectionButtons}>
        <GithubButton>GitHubで参加する</GithubButton>
      </div>
    </SectionWrapper>
  );
}
