"use client";

import { FormEvent, useState } from "react";
import {
  AlertCircle,
  CheckCircle2,
  KeyRound,
  LoaderCircle,
  Mail,
  Save,
  UserRound,
} from "lucide-react";
import { useRouter } from "next/navigation";

export function AdminProfileForm({
  initialName,
  initialEmail,
}: {
  initialName: string;
  initialEmail: string;
}) {
  const router = useRouter();
  const [pending, setPending] = useState(false);
  const [feedback, setFeedback] = useState<{
    type: "success" | "error";
    message: string;
  } | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setPending(true);
    setFeedback(null);

    const form = event.currentTarget;
    const formData = new FormData(form);

    try {
      const response = await fetch("/api/admin/profile", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: formData.get("name"),
          email: formData.get("email"),
          currentPassword: formData.get("currentPassword"),
          newPassword: formData.get("newPassword"),
          confirmPassword: formData.get("confirmPassword"),
        }),
      });
      const result = (await response.json()) as {
        message?: string;
      };

      if (!response.ok) {
        setFeedback({
          type: "error",
          message: result.message || "Your profile could not be updated.",
        });
        return;
      }

      setFeedback({
        type: "success",
        message: result.message || "Profile updated successfully.",
      });
      for (const fieldName of [
        "currentPassword",
        "newPassword",
        "confirmPassword",
      ]) {
        const field = form.elements.namedItem(fieldName);
        if (field instanceof HTMLInputElement) field.value = "";
      }
      router.refresh();
    } catch {
      setFeedback({
        type: "error",
        message: "Could not connect to the server. Please try again.",
      });
    } finally {
      setPending(false);
    }
  }

  return (
    <form className="admin-profile-form" onSubmit={handleSubmit}>
      <section className="admin-settings-card">
        <header>
          <span><UserRound aria-hidden /></span>
          <div>
            <h2>Profile information</h2>
            <p>Update the name and email associated with this account.</p>
          </div>
        </header>

        <div className="admin-settings-fields">
          <label>
            <span>Display name</span>
            <div>
              <UserRound aria-hidden />
              <input
                name="name"
                type="text"
                defaultValue={initialName}
                minLength={2}
                maxLength={100}
                autoComplete="name"
                required
              />
            </div>
          </label>
          <label>
            <span>Email address</span>
            <div>
              <Mail aria-hidden />
              <input
                name="email"
                type="email"
                defaultValue={initialEmail}
                maxLength={254}
                autoComplete="email"
                required
              />
            </div>
          </label>
        </div>
      </section>

      <section className="admin-settings-card">
        <header>
          <span><KeyRound aria-hidden /></span>
          <div>
            <h2>Password & security</h2>
            <p>Leave the new password fields empty to keep your current password.</p>
          </div>
        </header>

        <div className="admin-settings-fields password-grid">
          <label className="full">
            <span>Current password</span>
            <div>
              <KeyRound aria-hidden />
              <input
                name="currentPassword"
                type="password"
                autoComplete="current-password"
                placeholder="Required to save any changes"
                required
              />
            </div>
          </label>
          <label>
            <span>New password</span>
            <div>
              <KeyRound aria-hidden />
              <input
                name="newPassword"
                type="password"
                minLength={12}
                autoComplete="new-password"
                placeholder="At least 12 characters"
              />
            </div>
          </label>
          <label>
            <span>Confirm new password</span>
            <div>
              <KeyRound aria-hidden />
              <input
                name="confirmPassword"
                type="password"
                minLength={12}
                autoComplete="new-password"
                placeholder="Repeat the new password"
              />
            </div>
          </label>
        </div>
      </section>

      <div className="admin-settings-submit">
        <div
          className={`admin-settings-feedback ${feedback?.type || ""}`}
          role="status"
          aria-live="polite"
        >
          {feedback?.type === "success" && <CheckCircle2 aria-hidden />}
          {feedback?.type === "error" && <AlertCircle aria-hidden />}
          {feedback?.message}
        </div>
        <button type="submit" disabled={pending}>
          {pending ? (
            <LoaderCircle className="admin-spinner" aria-hidden />
          ) : (
            <Save aria-hidden />
          )}
          {pending ? "Saving changes..." : "Save changes"}
        </button>
      </div>
    </form>
  );
}
