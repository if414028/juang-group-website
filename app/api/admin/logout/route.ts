import { deleteAdminSession } from "@/lib/admin-auth";

export async function POST() {
  await deleteAdminSession();
  return new Response(null, {
    status: 303,
    headers: {
      Location: "/admin/login",
    },
  });
}
