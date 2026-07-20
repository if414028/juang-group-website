"use client";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { navigation } from "@/data/site";
import { useLanguage } from "@/components/language-provider";

export function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const { locale, setLocale, t } = useLanguage();
  const switcher = <div className="language-switcher" role="group" aria-label={locale === "id" ? "Pilih bahasa" : "Choose language"}><button className={locale === "en" ? "active" : ""} aria-pressed={locale === "en"} onClick={() => setLocale("en")}>EN</button><button className={locale === "id" ? "active" : ""} aria-pressed={locale === "id"} onClick={() => setLocale("id")}>ID</button></div>;
  return <header className="navbar"><div className="nav-inner"><Link className="brand" href="/" onClick={() => setOpen(false)} aria-label="Juang Group home"><span>J</span><strong>Juang Group</strong></Link><div className="nav-actions"><nav className="desktop-nav" aria-label={t("Main navigation")}>{navigation.map((item) => <Link key={item.href} aria-current={pathname === item.href ? "page" : undefined} className={pathname === item.href ? "active" : ""} href={item.href}>{t(item.label)}</Link>)}</nav><div className="desktop-language">{switcher}</div><button className="menu-button" aria-label={t(open ? "Close menu" : "Open menu")} aria-expanded={open} aria-controls="mobile-navigation" onClick={() => setOpen(!open)}>{open ? <X aria-hidden /> : <Menu aria-hidden />}</button></div></div>{open && <nav id="mobile-navigation" className="mobile-nav" aria-label={t("Mobile navigation")}>{navigation.map((item) => <Link key={item.href} aria-current={pathname === item.href ? "page" : undefined} className={pathname === item.href ? "active" : ""} href={item.href} onClick={() => setOpen(false)}>{t(item.label)}</Link>)}<div className="mobile-language">{switcher}</div></nav>}</header>;
}
