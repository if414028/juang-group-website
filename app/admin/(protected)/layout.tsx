import { AdminSidebar } from "@/components/admin-sidebar";
import { requireAdminSession } from "@/lib/admin-auth";

export default async function ProtectedAdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await requireAdminSession();

  return (
    <div className="admin-shell">
      <AdminSidebar email={session.email} />

      <div className="admin-content">{children}</div>
    </div>
  );
}
