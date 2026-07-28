import Link from "next/link";
import { ArrowLeft, CalendarDays, Mail, UserRound } from "lucide-react";
import { notFound } from "next/navigation";
import { AdminMessageActions } from "@/components/admin-message-actions";
import { formatJakartaDate } from "@/lib/format";
import { getContactMessage, setMessageStatus } from "@/lib/messages";

export const dynamic = "force-dynamic";

export default async function AdminMessagePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id: rawId } = await params;
  const id = Number(rawId);
  if (!Number.isSafeInteger(id) || id < 1) notFound();

  const message = await getContactMessage(id);
  if (!message) notFound();

  if (message.status === "unread") {
    await setMessageStatus(id, "read");
    message.status = "read";
    message.readAt = new Date();
  }

  return (
    <main className="admin-dashboard">
      <Link className="admin-back-link" href="/admin">
        <ArrowLeft aria-hidden />
        Back to inbox
      </Link>

      <article className="admin-message-detail">
        <header>
          <div>
            <p className="admin-kicker">PESAN #{message.id}</p>
            <h1>{message.subject}</h1>
          </div>
          <span className={`admin-status-pill ${message.status}`}>
            {message.status === "read" ? "Read" : "Unread"}
          </span>
        </header>

        <div className="admin-message-meta">
          <p>
            <UserRound aria-hidden />
            <span><small>Sender</small><strong>{message.name}</strong></span>
          </p>
          <p>
            <Mail aria-hidden />
            <span><small>Email</small><a href={`mailto:${message.email}`}>{message.email}</a></span>
          </p>
          <p>
            <CalendarDays aria-hidden />
            <span><small>Received</small><time dateTime={message.createdAt.toISOString()}>{formatJakartaDate(message.createdAt)}</time></span>
          </p>
        </div>

        <div className="admin-message-body">
          {message.message.split("\n").map((paragraph, index) => (
            <p key={`${message.id}-${index}`}>{paragraph || "\u00A0"}</p>
          ))}
        </div>

        <AdminMessageActions
          id={message.id}
          status={message.status}
          email={message.email}
        />
      </article>
    </main>
  );
}
