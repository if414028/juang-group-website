import Link from "next/link";
import { Inbox, LogOut, ShieldCheck } from "lucide-react";
import { requireAdminSession } from "@/lib/admin-auth";

export default async function ProtectedAdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await requireAdminSession();

  return (
    <div className="admin-shell">
      <aside className="admin-sidebar">
        <Link className="admin-sidebar-brand" href="/admin">
          <span className="admin-logo" aria-hidden />
          <span>
            <strong>Juang Group</strong>
            <small>Message Centre</small>
          </span>
        </Link>

        <nav aria-label="Admin navigation">
          <Link href="/admin">
            <Inbox aria-hidden />
            Inbox
          </Link>
        </nav>

        <div className="admin-sidebar-footer">
          <p>
            <ShieldCheck aria-hidden />
            <span>
              <small>Signed in as</small>
              <strong>{session.email}</strong>
            </span>
          </p>
          <form action="/api/admin/logout" method="post">
            <button type="submit">
              <LogOut aria-hidden />
              Sign out
            </button>
          </form>
        </div>
      </aside>

      <div className="admin-content">{children}</div>
    </div>
  );
}
