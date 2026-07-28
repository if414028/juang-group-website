import type { Metadata } from "next";
import { Mail, MessageSquareText, Send } from "lucide-react";
import { ContactForm } from "@/components/contact-form";

export const metadata: Metadata = {
  title: "Contact",
  description:
    "Send Juang Group a message about business, partnership, or investment opportunities.",
};

export default function ContactPage() {
  return (
    <section className="contact-page section">
      <div className="container contact-layout">
        <div className="contact-intro">
          <p className="eyebrow">Contact Juang Group</p>
          <h1>Start a thoughtful conversation.</h1>
          <p className="lead">
            For business, strategic partnership, or investment enquiries, Juang
            Group welcomes aligned conversations.
          </p>

          <div className="contact-points" aria-label="Contact information">
            <div>
              <span aria-hidden>
                <MessageSquareText />
              </span>
              <p>
                <strong>Send a direct message</strong>
                <small>Your message goes directly to our team.</small>
              </p>
            </div>
            <div>
              <span aria-hidden>
                <Mail />
              </span>
              <p>
                <strong>Personal response</strong>
                <small>We will reply to the email address you provide.</small>
              </p>
            </div>
            <div>
              <span aria-hidden>
                <Send />
              </span>
              <p>
                <strong>Clear and confidential</strong>
                <small>Share only the information relevant to your enquiry.</small>
              </p>
            </div>
          </div>
        </div>

        <ContactForm />
      </div>
    </section>
  );
}
