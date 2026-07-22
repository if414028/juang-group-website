import { Coffee } from "lucide-react";
import Image from "next/image";
import { ButtonLink } from "@/components/ui";

export function UnderDevelopmentPage({ name, description, symbol, image, imageAlt }: { name: string; description: string; symbol: string; image: string; imageAlt: string }) {
  return <section className="under-dev section"><div className="container under-grid"><div><p className="eyebrow">A Juang Group business</p><span className="badge in-development">In Development</span><h1>{name}</h1><p className="lead">{description}</p><p>The concept is being developed carefully. More information will be shared when its direction is ready.</p><div className="actions"><ButtonLink href="/">Back to Juang Group</ButtonLink><ButtonLink href="/yeshua-cafe" variant="outline">Explore Yeshua Cafe</ButtonLink></div></div><figure className="concept-illustration"><Image src={image} alt={imageAlt} fill priority sizes="(max-width: 900px) 100vw, 44vw" /><figcaption><span>{symbol}</span><Coffee aria-hidden /><small>Concept in progress</small></figcaption></figure></div></section>;
}
