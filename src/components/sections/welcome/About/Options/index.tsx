import styles from './styles.module.scss';

import OptionsList from './OptionsList';

export default function Options() {
  return (
    <div className={styles.section}>
      <div>
        <OptionsList title="クライアント側のオプション" dataKey="clientSide" />
        <OptionsList title="デプロイメント オプション" dataKey="deployment" />
        <OptionsList title="CI/CD オプション" dataKey="cicd" />
      </div>
      <div>
        <OptionsList title="サーバ側のオプション" dataKey="serverSide" />
      </div>
    </div>
  );
}
