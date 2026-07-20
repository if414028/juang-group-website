import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import { Footer } from "@/components/footer";
import { LanguageProvider, LocalizedContent } from "@/components/language-provider";
import { LocalizedText } from "@/components/localized-text";
import { Navbar } from "@/components/navbar";
import "./globals.css";

const manrope = Manrope({ subsets: ["latin"], variable: "--font-primary" });
const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  icons: {
    icon: [{ url: "/brand/official/juang-group-logo.svg", type: "image/svg+xml" }],
    shortcut: "/brand/official/juang-group-logo.svg",
    apple: "/brand/official/juang-group-logo.svg",
  },
  title: { default: "Juang Group | African–Indonesian Lifestyle & Entertainment", template: "%s | Juang Group" },
  description: "Founded and chaired by Ikenna Justin Ogidi, known as Justin Juang, Juang Group operates across hospitality, entertainment, consumer products, trading, and investment in Indonesia and Africa.",
  openGraph: { type: "website", siteName: "Juang Group", title: "Juang Group | African–Indonesian Lifestyle & Entertainment", description: "Building recognizable hospitality, lifestyle, and consumer brands across Indonesia and Africa." },
  twitter: { card: "summary_large_image", title: "Juang Group", description: "Building recognizable hospitality, lifestyle, and consumer brands across Indonesia and Africa." },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en" data-scroll-behavior="smooth" className={manrope.variable} suppressHydrationWarning><body><LanguageProvider><a className="skip-link" href="#main"><LocalizedText>Skip to content</LocalizedText></a><Navbar /><main id="main"><LocalizedContent>{children}</LocalizedContent></main><Footer /></LanguageProvider></body></html>;
}
