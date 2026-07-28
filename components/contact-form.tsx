"use client";

import { FormEvent, useState } from "react";
import { AlertCircle, CheckCircle2, LoaderCircle, Send } from "lucide-react";
import { useLanguage } from "@/components/language-provider";

type FormStatus = {
  type: "idle" | "success" | "error";
  message: string;
};

const initialStatus: FormStatus = { type: "idle", message: "" };

export function ContactForm() {
  const { t } = useLanguage();
  const [status, setStatus] = useState<FormStatus>(initialStatus);
  const [isSending, setIsSending] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSending(true);
    setStatus(initialStatus);

    const form = event.currentTarget;
    const formData = new FormData(form);

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(formData)),
      });
      const result = (await response.json()) as { message?: string };

      if (!response.ok) {
        throw new Error(result.message || t("Your message could not be sent."));
      }

      form.reset();
      setStatus({
        type: "success",
        message: t("Thank you. Your message has been saved successfully."),
      });
    } catch (error) {
      setStatus({
        type: "error",
        message:
          error instanceof Error
            ? error.message
            : t("Your message could not be sent."),
      });
    } finally {
      setIsSending(false);
    }
  }

  return (
    <form className="contact-form" onSubmit={handleSubmit}>
      <div className="contact-form-heading">
        <span aria-hidden>
          <Send />
        </span>
        <div>
          <p className="eyebrow">{t("Instant message")}</p>
          <h2>{t("Tell us what you have in mind.")}</h2>
        </div>
      </div>

      <div className="contact-form-grid">
        <div className="form-field">
          <label htmlFor="contact-name">{t("Full name")}</label>
          <input
            id="contact-name"
            name="name"
            type="text"
            autoComplete="name"
            maxLength={100}
            placeholder={t("Your full name")}
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="contact-email">{t("Email address")}</label>
          <input
            id="contact-email"
            name="email"
            type="email"
            inputMode="email"
            autoComplete="email"
            maxLength={254}
            placeholder={t("you@example.com")}
            required
          />
        </div>

        <div className="form-field form-field-wide">
          <label htmlFor="contact-subject">{t("Subject")}</label>
          <input
            id="contact-subject"
            name="subject"
            type="text"
            maxLength={150}
            placeholder={t("Business, partnership, or investment")}
            required
          />
        </div>

        <div className="form-field form-field-wide">
          <label htmlFor="contact-message">{t("Message")}</label>
          <textarea
            id="contact-message"
            name="message"
            rows={7}
            minLength={10}
            maxLength={5000}
            placeholder={t("Write your message here...")}
            required
          />
          <small>{t("Please include enough detail so we can respond clearly.")}</small>
        </div>

        <div className="contact-trap" hidden>
          <label htmlFor="contact-website">Website</label>
          <input
            id="contact-website"
            name="website"
            type="text"
            tabIndex={-1}
            autoComplete="off"
          />
        </div>
      </div>

      <div className="contact-form-actions">
        <button className="contact-submit" type="submit" disabled={isSending}>
          {isSending ? (
            <>
              <LoaderCircle className="contact-spinner" aria-hidden />
              {t("Sending message...")}
            </>
          ) : (
            <>
              <Send aria-hidden />
              {t("Send message")}
            </>
          )}
        </button>

        <p
          className={`contact-form-status ${status.type}`}
          role={status.type === "error" ? "alert" : "status"}
          aria-live="polite"
        >
          {status.type === "success" && <CheckCircle2 aria-hidden />}
          {status.type === "error" && <AlertCircle aria-hidden />}
          {status.message}
        </p>
      </div>
    </form>
  );
}
