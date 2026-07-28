"use client";
import Link from "next/link";
import { navigation } from "@/data/site";
import { useLanguage } from "@/components/language-provider";

export function Footer() {
  const { t } = useLanguage();
  return <footer className="footer"><div className="container footer-grid"><div><Link className="brand footer-brand" href="/"><span>J</span><strong>Juang Group</strong></Link><p>{t("Building commercially thoughtful businesses around culture, community, creativity, and purpose.")}</p></div><div><h2>{t("Explore")}</h2><div className="footer-links">{navigation.map((item) => <Link key={item.href} href={item.href}>{t(item.label)}</Link>)}</div></div><div><h2>{t("Business enquiries")}</h2><p>{t("Send us a direct message and our team will respond by email.")}</p><Link className="text-link light-link" href="/contact">{t("Connect with Juang Group")}</Link></div></div><div className="container footer-bottom"><span>© {new Date().getFullYear()}. All rights reserved. Powered by <a href="https://neshertechnology.id/" target="_blank" rel="noopener noreferrer">Nesher Teknologi Nusantara</a>.</span></div></footer>;
}
