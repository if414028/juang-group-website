import { getAdminSession } from "@/lib/admin-auth";
import {
  deleteContactMessage,
  setMessageStatus,
  type MessageStatus,
} from "@/lib/messages";

function parseId(value: string) {
  const id = Number(value);
  return Number.isSafeInteger(id) && id > 0 ? id : null;
}

async function authorize() {
  return Boolean(await getAdminSession());
}

export async function PATCH(
  request: Request,
  context: RouteContext<"/api/admin/messages/[id]">,
) {
  if (!(await authorize())) {
    return Response.json({ message: "Unauthorized." }, { status: 401 });
  }

  const { id: rawId } = await context.params;
  const id = parseId(rawId);
  if (!id) return Response.json({ message: "Invalid ID." }, { status: 400 });

  let body: { status?: unknown };
  try {
    body = (await request.json()) as typeof body;
  } catch {
    return Response.json({ message: "Invalid request." }, { status: 400 });
  }

  const status: MessageStatus | null =
    body.status === "read" || body.status === "unread" ? body.status : null;
  if (!status) {
    return Response.json({ message: "Invalid status." }, { status: 400 });
  }

  const updated = await setMessageStatus(id, status);
  return updated
    ? Response.json({ success: true })
    : Response.json({ message: "Message not found." }, { status: 404 });
}

export async function DELETE(
  _request: Request,
  context: RouteContext<"/api/admin/messages/[id]">,
) {
  if (!(await authorize())) {
    return Response.json({ message: "Unauthorized." }, { status: 401 });
  }

  const { id: rawId } = await context.params;
  const id = parseId(rawId);
  if (!id) return Response.json({ message: "Invalid ID." }, { status: 400 });

  const deleted = await deleteContactMessage(id);
  return deleted
    ? Response.json({ success: true })
    : Response.json({ message: "Message not found." }, { status: 404 });
}
