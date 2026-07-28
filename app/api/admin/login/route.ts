import { compare } from "bcryptjs";
import { createAdminSession } from "@/lib/admin-auth";
import { getAdminByEmail, updateAdminLastLogin } from "@/lib/admin-users";

type Attempt = { count: number; resetAt: number };

declare global {
  var juangLoginAttempts: Map<string, Attempt> | undefined;
}

const attempts =
  globalThis.juangLoginAttempts ||
  (globalThis.juangLoginAttempts = new Map<string, Attempt>());

function getClientIp(request: Request) {
  return (
    request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
    request.headers.get("x-real-ip") ||
    "unknown"
  );
}

function isRateLimited(ip: string) {
  const now = Date.now();
  const attempt = attempts.get(ip);
  if (!attempt || attempt.resetAt < now) {
    attempts.set(ip, { count: 0, resetAt: now + 15 * 60 * 1000 });
    return false;
  }
  return attempt.count >= 8;
}

function recordFailure(ip: string) {
  const current = attempts.get(ip);
  attempts.set(ip, {
    count: (current?.count || 0) + 1,
    resetAt: current?.resetAt || Date.now() + 15 * 60 * 1000,
  });
}

export async function POST(request: Request) {
  const ip = getClientIp(request);
  if (isRateLimited(ip)) {
    return Response.json(
      { message: "Too many attempts. Please try again in 15 minutes." },
      { status: 429 },
    );
  }

  let input: { email?: unknown; password?: unknown };
  try {
    input = (await request.json()) as typeof input;
  } catch {
    return Response.json({ message: "Invalid request." }, { status: 400 });
  }

  const email =
    typeof input.email === "string" ? input.email.trim().toLowerCase() : "";
  const password = typeof input.password === "string" ? input.password : "";

  if (!email || !password || password.length > 200) {
    return Response.json(
      { message: "Email and password are required." },
      { status: 400 },
    );
  }

  try {
    const admin = await getAdminByEmail(email);
    const passwordMatches =
      admin?.isActive && (await compare(password, admin.passwordHash));

    if (!admin || !passwordMatches) {
      recordFailure(ip);
      await new Promise((resolve) => setTimeout(resolve, 500));
      return Response.json(
        { message: "Incorrect email or password." },
        { status: 401 },
      );
    }

    await createAdminSession({ id: admin.id, email: admin.email });
    await updateAdminLastLogin(admin.id);
    attempts.delete(ip);

    return Response.json({ success: true });
  } catch (error) {
    console.error("Admin login failed:", error);
    return Response.json(
      { message: "Login could not be processed. Check the server configuration." },
      { status: 503 },
    );
  }
}
