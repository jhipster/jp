export const books = [
  {
    title: 'JHipsterミニブック 7.0',
    authors: ['Matt Raible'],
    image: require('/images/books/JHipster-Mini-book.webp').default,
    description:
      'JHipsterミニブックは、Angular、Bootstrap、Spring Bootといった最新技術の入門ガイドです。これらのフレームワークは、使いやすいプロジェクトであるJHipsterにまとめられています。この版では、WebFluxやReactを用いたマイクロフロントエンドを特徴とするマイクロサービスセクションが更新されています。',
    links: [
      {
        name: 'InfoQ',
        href: 'https://www.infoq.com/minibooks/jhipster-mini-book-7',
      },
    ],
  },
  {
    title: 'JHipsterによるフルスタック開発 - 第2版',
    authors: ['Deepu K Sasidharan', 'Sendil Kumar'],
    image: require('/images/books/Full-Stack-Development-with-JHipster.webp')
      .default,
    description:
      'JHipsterのコア開発チームによって執筆され、JHipster 6、Java 11、Spring Boot 2.1に完全対応したこの書籍は、実践的な例とベストプラクティスを通じて、モダンなウェブアプリケーションの構築方法を紹介します。',
    links: [
      {
        name: 'Packt',
        href: 'https://www.packtpub.com/web-development/full-stack-development-with-jhipster-second-edition',
      },
      {
        name: 'Amazon',
        href: 'https://smile.amazon.com/Full-Stack-Development-JHipster-microservices/dp/1838824987',
      },
    ],
  },
];
