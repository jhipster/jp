import Link from '@docusaurus/Link';
import AutoScroll from 'embla-carousel-auto-scroll';

import {
  SectionDescription,
  SectionTitle,
} from '@site/src/components/ui/SectionWrapper';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
} from '@site/src/components/ui/Carousel';
import CompanyLogo from './CompanyLogo';
import styles from './styles.module.scss';

import companies from '@site/src/data/companies.json';

const filteredCompanies = companies.filter((company) => !!company.logo);
const logosListsDivider = 30;

export default function WhoUses() {
  return (
    <section className={styles.section}>
      <div className="container">
        <SectionTitle>誰がJHipsterを使用していますか?</SectionTitle>

        <SectionDescription>
        世界中で多くの優れた企業がJHipsterを使用しています！
          <Link
            className="text-foreground underline"
            href="/companies-using-jhipster"
          >
            全リストはこちら。 
          </Link>
          JHipsterを使用を開始したら忘れずにここに登録をお願いいたします。
        </SectionDescription>
      </div>

      <Carousel
        className={styles.carousel}
        opts={{ align: 'center', loop: true }}
        plugins={[AutoScroll({ speed: 1, stopOnInteraction: false })]}
      >
        <CarouselContent>
          {filteredCompanies.slice(0, logosListsDivider).map((company, idx) => (
            <CarouselItem key={`users-${idx}`} className={styles.carouselItem}>
              <CompanyLogo company={company} />
            </CarouselItem>
          ))}
        </CarouselContent>
      </Carousel>

      <Carousel
        className={styles.carousel}
        opts={{ align: 'center', loop: true }}
        plugins={[AutoScroll({ speed: 0.75, stopOnInteraction: false })]}
      >
        <CarouselContent>
          {filteredCompanies.slice(logosListsDivider).map((company, idx) => (
            <CarouselItem key={`users-${idx}`} className={styles.carouselItem}>
              <CompanyLogo company={company} />
            </CarouselItem>
          ))}
        </CarouselContent>
      </Carousel>
    </section>
  );
}
