import { createContactMessage } from "@/lib/messages";

type ContactPayload = {
  name?: unknown;
  email?: unknown;
  subject?: unknown;
  message?: unknown;
  website?: unknown;
};

type ContactAttempt = { count: number; resetAt: number };

declare global {
  var juangContactAttempts: Map<string, ContactAttempt> | undefined;
}

const attempts =
  globalThis.juangContactAttempts ||
  (globalThis.juangContactAttempts = new Map<string, ContactAttempt>());

function cleanText(value: unknown, maxLength: number) {
  return typeof value === "string" ? value.trim().slice(0, maxLength) : "";
}

function isValidEmail(value: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function getClientIp(request: Request) {
  return (
    request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
    request.headers.get("x-real-ip") ||
    null
  );
}

function isRateLimited(key: string) {
  const now = Date.now();
  const current = attempts.get(key);
  if (!current || current.resetAt < now) {
    attempts.set(key, { count: 1, resetAt: now + 60 * 60 * 1000 });
    return false;
  }

  if (current.count >= 10) return true;
  current.count += 1;
  return false;
}

export async function POST(request: Request) {
  const contentType = request.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    return Response.json(
      { message: "Invalid request format." },
      { status: 415 },
    );
  }

  let payload: ContactPayload;
  try {
    payload = (await request.json()) as ContactPayload;
  } catch {
    return Response.json({ message: "Invalid message data." }, { status: 400 });
  }

  if (cleanText(payload.website, 200)) {
    return Response.json({ message: "Message received." });
  }

  const name = cleanText(payload.name, 100);
  const email = cleanText(payload.email, 254).toLowerCase();
  const subject = cleanText(payload.subject, 150);
  const message = cleanText(payload.message, 5000);

  if (
    name.length < 2 ||
    !isValidEmail(email) ||
    subject.length < 3 ||
    message.length < 10
  ) {
    return Response.json(
      { message: "Please complete all fields with valid information." },
      { status: 400 },
    );
  }

  const ipAddress = getClientIp(request);
  const rateLimitKey = ipAddress || email;
  if (isRateLimited(rateLimitKey)) {
    return Response.json(
      { message: "Too many messages. Please try again later." },
      { status: 429 },
    );
  }

  try {
    await createContactMessage({
      name,
      email,
      subject,
      message,
      ipAddress,
      userAgent: cleanText(request.headers.get("user-agent"), 500) || null,
    });

    return Response.json({
      message: "Thank you. Your message has been saved successfully.",
    });
  } catch (error) {
    console.error("Saving contact message failed:", error);
    return Response.json(
      { message: "Your message could not be saved. Please try again." },
      { status: 503 },
    );
  }
}
