import { deleteAdminSession } from "@/lib/admin-auth";

export async function POST(request: Request) {
  await deleteAdminSession();
  return Response.redirect(new URL("/admin/login", request.url), 303);
}
