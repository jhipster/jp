import { ChangeEvent } from 'react';
import Heading from '@theme/Heading';

import SearchInput from '@site/src/components/SearchInput';
import styles from './styles.module.scss';
import Link from '@docusaurus/Link';

type Props = {
  value: string;
  numberFilteredModules: number;
  numberModules: number;
  handleSearch: (event: ChangeEvent<HTMLInputElement>) => void;
};

export default function MarketplaceHero({
  value,
  numberFilteredModules = 0,
  numberModules = 0,
  handleSearch,
}: Props) {
  return (
    <header className={styles.section}>
      <div className="container">
        <Heading className={styles.sectionTitle} as="h1">
          マーケットプレイス
        </Heading>

        <Heading as="h2">
          利用可能なモジュールとブループリント (
          {`${numberFilteredModules}/${numberModules}`})
        </Heading>

        <SearchInput
          value={value}
          placeholder="名前やキーワードでフィルタリング"
          onInput={handleSearch}
        />

        <div className={styles.sectionButtons}>
          <Link
            className="button button--primary"
            to="/modules/creating-a-module"
          >
            独自のモジュールを作成
          </Link>
          <Link
            className="button button--secondary"
            to="/modules/creating-a-blueprint"
          >
            独自のブループリントを作成
          </Link>
        </div>
      </div>
    </header>
  );
}
