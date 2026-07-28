import Link from "next/link";
import {
  ArrowRight,
  Inbox,
  MailCheck,
  MailOpen,
  Search,
} from "lucide-react";
import { formatJakartaDate } from "@/lib/format";
import {
  getMessageCounts,
  listContactMessages,
  type MessageStatus,
} from "@/lib/messages";

export const dynamic = "force-dynamic";

type DashboardSearchParams = Promise<{
  status?: string;
  q?: string;
}>;

function cleanStatus(value?: string): MessageStatus | "all" {
  return value === "read" || value === "unread" ? value : "all";
}

export default async function AdminDashboardPage({
  searchParams,
}: {
  searchParams: DashboardSearchParams;
}) {
  const params = await searchParams;
  const status = cleanStatus(params.status);
  const query = typeof params.q === "string" ? params.q.trim().slice(0, 100) : "";
  const [counts, messages] = await Promise.all([
    getMessageCounts(),
    listContactMessages({ status, query, limit: 100 }),
  ]);

  return (
    <main className="admin-dashboard">
      <header className="admin-page-header">
        <div>
          <p className="admin-kicker">MESSAGE CENTRE</p>
          <h1>Dashboard</h1>
          <p>Messages submitted through the Juang Group contact page.</p>
        </div>
        <span className="admin-live-badge">
          <i aria-hidden />
          Connected to website
        </span>
      </header>

      <section className="admin-stats" aria-label="Inbox summary">
        <article>
          <span>
            <Inbox aria-hidden />
          </span>
          <p>Total messages<strong>{counts.total}</strong></p>
        </article>
        <article>
          <span>
            <MailOpen aria-hidden />
          </span>
          <p>Unread<strong>{counts.unread}</strong></p>
        </article>
        <article>
          <span>
            <MailCheck aria-hidden />
          </span>
          <p>Read<strong>{counts.read}</strong></p>
        </article>
      </section>

      <section className="admin-inbox-card">
        <div className="admin-inbox-toolbar">
          <div className="admin-filter-tabs" aria-label="Filter message status">
            <Link className={status === "all" ? "active" : ""} href="/admin">
              All
            </Link>
            <Link
              className={status === "unread" ? "active" : ""}
              href="/admin?status=unread"
            >
              Unread
            </Link>
            <Link
              className={status === "read" ? "active" : ""}
              href="/admin?status=read"
            >
              Read
            </Link>
          </div>

          <form className="admin-search" action="/admin" method="get">
            {status !== "all" && (
              <input type="hidden" name="status" value={status} />
            )}
            <Search aria-hidden />
            <label className="sr-only" htmlFor="message-search">
              Search messages
            </label>
            <input
              id="message-search"
              name="q"
              type="search"
              defaultValue={query}
              placeholder="Search name, email, or subject..."
            />
          </form>
        </div>

        {messages.length ? (
          <div className="admin-message-list">
            {messages.map((message) => (
              <Link
                className={`admin-message-row ${message.status}`}
                href={`/admin/messages/${message.id}`}
                key={message.id}
              >
                <span className="admin-message-avatar" aria-hidden>
                  {message.name.slice(0, 1).toUpperCase()}
                </span>
                <span className="admin-message-sender">
                  <strong>{message.name}</strong>
                  <small>{message.email}</small>
                </span>
                <span className="admin-message-preview">
                  <strong>{message.subject}</strong>
                  <small>{message.message}</small>
                </span>
                <time dateTime={message.createdAt.toISOString()}>
                  {formatJakartaDate(message.createdAt)}
                </time>
                <ArrowRight aria-hidden />
              </Link>
            ))}
          </div>
        ) : (
          <div className="admin-empty-state">
            <Inbox aria-hidden />
            <h2>No messages yet</h2>
            <p>
              {query || status !== "all"
                ? "No messages match the current filter."
                : "New messages from the contact page will appear here."}
            </p>
          </div>
        )}
      </section>
    </main>
  );
}
