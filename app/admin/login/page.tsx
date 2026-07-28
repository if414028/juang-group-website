import { redirect } from "next/navigation";
import { AdminLoginForm } from "@/components/admin-login-form";
import { getAdminSession } from "@/lib/admin-auth";

export default async function AdminLoginPage() {
  if (await getAdminSession()) redirect("/admin");

  return (
    <section className="admin-login-page">
      <div className="admin-login-brand">
        <div className="admin-logo" aria-hidden />
        <p>JUANG GROUP</p>
        <span>Content Management System</span>
      </div>
      <AdminLoginForm />
      <small className="admin-login-note">
        This page is restricted to authorized users.
      </small>
    </section>
  );
}
