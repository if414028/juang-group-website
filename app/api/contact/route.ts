const recipientEmail =
  process.env.CONTACT_TO_EMAIL || "justinikenna08@gmail.com";

type ContactPayload = {
  name?: unknown;
  email?: unknown;
  subject?: unknown;
  message?: unknown;
  website?: unknown;
};

function cleanText(value: unknown, maxLength: number) {
  return typeof value === "string" ? value.trim().slice(0, maxLength) : "";
}

function escapeHtml(value: string) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function isValidEmail(value: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
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

  const apiKey = process.env.RESEND_API_KEY;
  const fromEmail = process.env.CONTACT_FROM_EMAIL;

  if (!apiKey || !fromEmail) {
    console.error(
      "Contact form is missing RESEND_API_KEY or CONTACT_FROM_EMAIL.",
    );
    return Response.json(
      {
        message:
          "The message service is not configured yet. Please try again later.",
      },
      { status: 503 },
    );
  }

  const safeName = escapeHtml(name);
  const safeEmail = escapeHtml(email);
  const safeSubject = escapeHtml(subject);
  const safeMessage = escapeHtml(message).replaceAll("\n", "<br />");

  try {
    const emailResponse = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: fromEmail,
        to: [recipientEmail],
        reply_to: email,
        subject: `[Juang Group Website] ${subject}`,
        html: `
          <div style="font-family:Arial,sans-serif;max-width:640px;margin:auto;color:#1e3932">
            <p style="font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#00754a">New website enquiry</p>
            <h1 style="font-size:28px;line-height:1.2">${safeSubject}</h1>
            <p><strong>From:</strong> ${safeName}</p>
            <p><strong>Email:</strong> <a href="mailto:${safeEmail}">${safeEmail}</a></p>
            <div style="margin-top:24px;padding:24px;background:#f2f0eb;border-left:4px solid #00754a;border-radius:8px;line-height:1.7">${safeMessage}</div>
          </div>
        `,
        text: `New website enquiry\n\nFrom: ${name}\nEmail: ${email}\nSubject: ${subject}\n\n${message}`,
      }),
    });

    if (!emailResponse.ok) {
      const providerError = await emailResponse.text();
      console.error("Resend contact email failed:", providerError);
      return Response.json(
        { message: "Your message could not be sent. Please try again." },
        { status: 502 },
      );
    }

    return Response.json({
      message: "Thank you. Your message has been sent successfully.",
    });
  } catch (error) {
    console.error("Contact email request failed:", error);
    return Response.json(
      { message: "Your message could not be sent. Please try again." },
      { status: 502 },
    );
  }
}
