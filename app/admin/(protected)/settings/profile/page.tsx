import { AdminProfileForm } from "@/components/admin-profile-form";
import { requireAdminSession } from "@/lib/admin-auth";
import { getAdminById } from "@/lib/admin-users";

export const dynamic = "force-dynamic";

export default async function AdminProfilePage() {
  const session = await requireAdminSession();
  const admin = await getAdminById(session.adminId);

  if (!admin?.isActive) {
    return null;
  }

  return (
    <main className="admin-dashboard admin-settings-page">
      <header className="admin-page-header">
        <div>
          <p className="admin-kicker">SETTINGS / PROFILE</p>
          <h1>Profile</h1>
          <p>Manage your account details and sign-in credentials.</p>
        </div>
      </header>

      <AdminProfileForm
        initialName={admin.name}
        initialEmail={admin.email}
      />
    </main>
  );
}
