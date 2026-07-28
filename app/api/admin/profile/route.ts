import { compare, hash } from "bcryptjs";
import { createAdminSession, getAdminSession } from "@/lib/admin-auth";
import { getAdminById, updateAdminProfile } from "@/lib/admin-users";

type ProfilePayload = {
  name?: unknown;
  email?: unknown;
  currentPassword?: unknown;
  newPassword?: unknown;
  confirmPassword?: unknown;
};

function text(value: unknown, maxLength: number) {
  return typeof value === "string" ? value.trim().slice(0, maxLength) : "";
}

function validEmail(value: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export async function PATCH(request: Request) {
  const session = await getAdminSession();
  if (!session) {
    return Response.json({ message: "Unauthorized." }, { status: 401 });
  }

  let input: ProfilePayload;
  try {
    input = (await request.json()) as ProfilePayload;
  } catch {
    return Response.json({ message: "Invalid request." }, { status: 400 });
  }

  const name = text(input.name, 100);
  const email = text(input.email, 254).toLowerCase();
  const currentPassword =
    typeof input.currentPassword === "string" ? input.currentPassword : "";
  const newPassword =
    typeof input.newPassword === "string" ? input.newPassword : "";
  const confirmPassword =
    typeof input.confirmPassword === "string" ? input.confirmPassword : "";

  if (name.length < 2 || !validEmail(email)) {
    return Response.json(
      { message: "Enter a valid name and email address." },
      { status: 400 },
    );
  }

  if (!currentPassword) {
    return Response.json(
      { message: "Your current password is required to save changes." },
      { status: 400 },
    );
  }

  if (newPassword && newPassword.length < 12) {
    return Response.json(
      { message: "The new password must contain at least 12 characters." },
      { status: 400 },
    );
  }

  if (newPassword !== confirmPassword) {
    return Response.json(
      { message: "The new password confirmation does not match." },
      { status: 400 },
    );
  }

  try {
    const admin = await getAdminById(session.adminId);
    if (!admin?.isActive) {
      return Response.json({ message: "Unauthorized." }, { status: 401 });
    }

    if (!(await compare(currentPassword, admin.passwordHash))) {
      return Response.json(
        { message: "Your current password is incorrect." },
        { status: 403 },
      );
    }

    await updateAdminProfile({
      id: admin.id,
      name,
      email,
      passwordHash: newPassword ? await hash(newPassword, 12) : undefined,
    });

    await createAdminSession({ id: admin.id, email });
    return Response.json({
      success: true,
      message: newPassword
        ? "Profile and password updated successfully."
        : "Profile updated successfully.",
    });
  } catch (error) {
    const databaseError = error as { code?: string };
    if (databaseError.code === "ER_DUP_ENTRY") {
      return Response.json(
        { message: "That email address is already in use." },
        { status: 409 },
      );
    }

    console.error("Updating admin profile failed:", error);
    return Response.json(
      { message: "Your profile could not be updated. Please try again." },
      { status: 503 },
    );
  }
}
