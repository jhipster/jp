import { useEffect, useRef, useState } from 'react';
import Link from '@docusaurus/Link';
import AutoScroll, {
  type AutoScrollOptionsType,
} from 'embla-carousel-auto-scroll';

import {
  SectionDescription,
  SectionTitle,
} from '@site/src/components/ui/SectionWrapper';
import {
  Carousel,
  CarouselApi,
  CarouselContent,
  CarouselItem,
} from '@site/src/components/ui/Carousel';
import CompanyLogo from './CompanyLogo';
import styles from './styles.module.scss';

import { useOnScreen } from '@site/src/hooks/use-onscreen';

import companies from '@site/src/data/companies.json';

const filteredCompanies = companies.filter((company) => !!company.logo);
const logosListsDivider = 30;
const commonAutoScrollOptions: AutoScrollOptionsType = {
  stopOnInteraction: false,
  playOnInit: false,
};

export default function WhoUses() {
  const ref = useRef(null);
  const isVisible = useOnScreen(ref);
  const [topApi, setTopApi] = useState<CarouselApi>();
  const [bottomApi, setBottomApi] = useState<CarouselApi>();

  useEffect(() => {
    if (!topApi || !bottomApi) {
      return;
    }

    if (isVisible) {
      topApi.plugins().autoScroll.play(0);
      bottomApi.plugins().autoScroll.play(0);
    } else {
      topApi.plugins().autoScroll.stop();
      bottomApi.plugins().autoScroll.stop();
    }
  }, [topApi, bottomApi, isVisible]);

  return (
    <section ref={ref} className={styles.section}>
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
        setApi={setTopApi}
        opts={{ align: 'center', loop: true }}
        plugins={[AutoScroll({ ...commonAutoScrollOptions, speed: 1 })]}
      >
        <CarouselContent>
          {filteredCompanies.slice(0, logosListsDivider).map((company, idx) => (
            <CarouselItem
              key={`companies-top-${idx}`}
              className={styles.carouselItem}
            >
              <CompanyLogo company={company} />
            </CarouselItem>
          ))}
        </CarouselContent>
      </Carousel>

      <Carousel
        className={styles.carousel}
        setApi={setBottomApi}
        opts={{ align: 'center', loop: true }}
        plugins={[AutoScroll({ ...commonAutoScrollOptions, speed: 0.75 })]}
      >
        <CarouselContent>
          {filteredCompanies.slice(logosListsDivider).map((company, idx) => (
            <CarouselItem
              key={`companies-bottom-${idx}`}
              className={styles.carouselItem}
            >
              <CompanyLogo company={company} />
            </CarouselItem>
          ))}
        </CarouselContent>
      </Carousel>
    </section>
  );
}
