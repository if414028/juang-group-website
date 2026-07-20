import Link from "next/link";
import Image from "next/image";
import { ArrowUpRight } from "lucide-react";
import type { BusinessUnit } from "@/data/site";

export function ButtonLink({ href, children, variant = "primary" }: { href: string; children: React.ReactNode; variant?: "primary" | "outline" | "light" | "light-outline" }) {
  return <Link className={`button button-${variant}`} href={href}>{children}</Link>;
}

export function SectionHeading({ eyebrow, title, body, light = false }: { eyebrow: string; title: string; body?: string; light?: boolean }) {
  return <div className={`section-heading ${light ? "light" : ""}`}><p className="eyebrow">{eyebrow}</p><h2>{title}</h2>{body && <p>{body}</p>}</div>;
}

export function FounderVisual() {
  return <figure className="founder-visual"><div className="founder-frame"><Image src="/images/founder/justin.webp" alt="Ikenna Justin Ogidi, known as Justin Juang, founder and chairman of Juang Group" fill priority sizes="(max-width: 900px) 100vw, 42vw" /><span>Founder &amp; Chairman</span></div><figcaption>Ikenna Justin Ogidi · Known as Justin Juang</figcaption></figure>;
}

export function UnitCard({ unit }: { unit: BusinessUnit }) {
  return <article className="unit-card"><div className="unit-top"><span className={`badge ${unit.status}`}>{unit.status === "featured" ? "Featured Concept" : "In Development"}</span><span className="unit-mark">{unit.mark}</span></div><h3>{unit.name}</h3><p>{unit.shortDescription}</p><Link className="text-link" href={unit.href}>{unit.status === "featured" ? "Explore Juang Cafe" : "View Concept"} <ArrowUpRight size={18} aria-hidden /></Link></article>;
}
