import type { Metadata } from "next";
import { Mail } from "lucide-react";
import { ButtonLink } from "@/components/ui";
export const metadata: Metadata = { title: "Contact", description: "Connect with Juang Group about business, partnership, or investment opportunities." };
export default function ContactPage() { return <section className="contact-page section"><div className="container contact-card"><div><p className="eyebrow">Contact Juang Group</p><h1>Start a thoughtful conversation.</h1><p className="lead">For business, strategic partnership, or investment enquiries, Juang Group welcomes aligned conversations.</p><p>Official contact details are being prepared and will be available soon. No message form is shown until a secure delivery channel is connected.</p><ButtonLink href="/yeshua-cafe">Explore Yeshua Cafe</ButtonLink></div><div className="contact-mark" aria-hidden><Mail /><span>Details<br />coming soon</span></div></div></section>; }
