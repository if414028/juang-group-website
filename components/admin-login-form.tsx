"use client";

import { FormEvent, useState } from "react";
import { AlertCircle, LoaderCircle, LockKeyhole, LogIn, Mail } from "lucide-react";
import { useRouter } from "next/navigation";

export function AdminLoginForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoading(true);
    setError("");

    const formData = new FormData(event.currentTarget);
    try {
      const response = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: formData.get("email"),
          password: formData.get("password"),
        }),
      });
      const result = (await response.json()) as { message?: string };

      if (!response.ok) {
        setError(result.message || "Login could not be processed.");
        return;
      }

      router.replace("/admin");
      router.refresh();
    } catch {
      setError("Could not connect to the server. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form className="admin-login-form" onSubmit={handleSubmit}>
      <div className="admin-login-heading">
        <span>
          <LockKeyhole aria-hidden />
        </span>
        <div>
          <p>ADMIN ACCESS</p>
          <h1>Sign in to Dashboard</h1>
        </div>
      </div>

      <div className="admin-field">
        <label htmlFor="admin-email">Admin email</label>
        <div>
          <Mail aria-hidden />
          <input
            id="admin-email"
            name="email"
            type="email"
            autoComplete="username"
            placeholder="admin@juanggroup.com"
            required
          />
        </div>
      </div>

      <div className="admin-field">
        <label htmlFor="admin-password">Password</label>
        <div>
          <LockKeyhole aria-hidden />
          <input
            id="admin-password"
            name="password"
            type="password"
            autoComplete="current-password"
            minLength={12}
            placeholder="Enter your password"
            required
          />
        </div>
      </div>

      <button className="admin-primary-button" type="submit" disabled={isLoading}>
        {isLoading ? (
          <>
            <LoaderCircle className="admin-spinner" aria-hidden />
            Signing in...
          </>
        ) : (
          <>
            <LogIn aria-hidden />
            Sign in
          </>
        )}
      </button>

      <p className="admin-form-error" role="alert" aria-live="polite">
        {error && <AlertCircle aria-hidden />}
        {error}
      </p>
    </form>
  );
}
