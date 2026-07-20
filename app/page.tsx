import Link from "next/link";
import Image from "next/image";
import { ArrowRight, Coffee, Hotel, ShoppingBag } from "lucide-react";
import { businessUnits, values } from "@/data/site";
import { ButtonLink, FounderVisual, SectionHeading, UnitCard } from "@/components/ui";

export default function Home() {
  return (
    <>
      <section className="hero section">
        <div className="container hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">Juang Group · Indonesia &amp; Africa</p>
            <p className="founder-line">Founded and chaired by Ikenna Justin Ogidi—widely known as Justin Juang.</p>
            <h1>A Lifestyle and Entertainment Group Built Across Cultures.</h1>
            <p className="lead">Juang Group is an African–Indonesian lifestyle and entertainment group with businesses spanning hospitality, dining, consumer products, trading, and investment. From Indonesia to Africa, the group continues to expand through brands designed for quality, relevance, and lasting impact.</p>
            <div className="actions">
              <ButtonLink href="/about">Discover Our Story</ButtonLink>
              <ButtonLink href="/juang-cafe" variant="outline">Explore Juang Cafe</ButtonLink>
            </div>
          </div>
          <FounderVisual />
        </div>
      </section>

      <section className="section surface-white">
        <div className="container split">
          <div className="portrait-note"><span>1985</span><p>the birth year of founder and chairman Ikenna Justin Ogidi</p></div>
          <div>
            <SectionHeading eyebrow="Meet the Founder" title="The builder behind Juang Group." />
            <p className="lead">A Nigerian builder, entrepreneur, and philanthropist, Justin graduated from Enugu State University of Science and Technology. His experience across Nigeria and Indonesia has shaped Juang Group into a recognizable cross-cultural lifestyle business.</p>
            <Link className="text-link" href="/about">Read Justin’s story <ArrowRight size={18} aria-hidden /></Link>
          </div>
        </div>
      </section>

      <section className="section dark-band">
        <div className="container">
          <SectionHeading eyebrow="Core Divisions" title="A diversified group with a lifestyle focus." light />
          <div className="three-grid">
            {[
              [Hotel, "Hospitality & Dining", "Cafes, restaurants, and entertainment-led hospitality brands across Indonesia and Nigeria, including Jakarta."],
              [ShoppingBag, "Consumer Products", "Food and beverage brands including Jinggle Bells Ice Creams, coffee, and chocolate products."],
              [Coffee, "Trading & Investment", "A commercial platform supporting product development, distribution, partnerships, and expansion into new industries."],
            ].map(([Icon, title, text]) => {
              const CardIcon = Icon as typeof Hotel;
              return <article className="dark-card" key={title as string}><CardIcon aria-hidden /><h3>{title as string}</h3><p>{text as string}</p></article>;
            })}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <SectionHeading eyebrow="Our Brand Ecosystem" title="From hospitality to consumer brands." body="Juang Group brings together complementary businesses with room to grow across Indonesia, Nigeria, and wider African markets." />
          <div className="units-grid">{businessUnits.map((unit) => <UnitCard key={unit.slug} unit={unit} />)}</div>
        </div>
      </section>

      <section className="section surface-ceramic">
        <div className="container">
          <SectionHeading eyebrow="Vision & Values" title="How Juang Group continues to grow." />
          <div className="values-grid">{values.map((value, index) => <article className="value-card" key={value.title}><span>0{index + 1}</span><h3>{value.title}</h3><p>{value.description}</p></article>)}</div>
        </div>
      </section>

      <section className="section surface-white">
        <div className="container feature">
          <div>
            <p className="eyebrow">Featured Business · Juang Cafe</p>
            <h2>A cafe brand built around inclusion.</h2>
            <p className="lead">Founded by Justin, Juang Cafe is growing across Jakarta and Indonesia with a defining mission: to create welcoming hospitality experiences while opening meaningful employment opportunities for people with Down syndrome, God willing.</p>
            <ButtonLink href="/juang-cafe">Explore the Full Concept</ButtonLink>
          </div>
          <figure className="feature-visual"><Image src="/images/juang-cafe/community-cafe.webp" alt="Editorial illustration of Juang Cafe as an open, welcoming and inclusive community space" fill sizes="(max-width: 900px) 100vw, 46vw" /><figcaption><span>J</span><p>Inclusive by purpose.<br />Growing with people.</p></figcaption></figure>
        </div>
      </section>

      <section className="section closing">
        <div className="container closing-inner"><div><p className="eyebrow">Growing across industries</p><h2>Building Recognizable Brands Across Indonesia and Africa.</h2></div><div className="actions"><ButtonLink href="/juang-cafe" variant="light">Explore Juang Cafe</ButtonLink><ButtonLink href="/contact" variant="light-outline">Connect With Us</ButtonLink></div></div>
      </section>
    </>
  );
}
