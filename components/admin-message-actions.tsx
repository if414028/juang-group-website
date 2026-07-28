"use client";

import { useState } from "react";
import { CheckCheck, LoaderCircle, Mail, Trash2 } from "lucide-react";
import { useRouter } from "next/navigation";
import type { MessageStatus } from "@/lib/messages";

export function AdminMessageActions({
  id,
  status,
  email,
}: {
  id: number;
  status: MessageStatus;
  email: string;
}) {
  const router = useRouter();
  const [pendingAction, setPendingAction] = useState<
    "status" | "delete" | null
  >(null);
  const [error, setError] = useState("");

  async function toggleStatus() {
    setPendingAction("status");
    setError("");
    try {
      const response = await fetch(`/api/admin/messages/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: status === "read" ? "unread" : "read" }),
      });
      if (!response.ok) throw new Error();
      if (status === "read") {
        router.replace("/admin");
      } else {
        router.refresh();
      }
    } catch {
      setError("The message status could not be updated.");
    } finally {
      setPendingAction(null);
    }
  }

  async function deleteMessage() {
    if (!window.confirm("Permanently delete this message?")) return;

    setPendingAction("delete");
    setError("");
    try {
      const response = await fetch(`/api/admin/messages/${id}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error();
      router.replace("/admin");
      router.refresh();
    } catch {
      setError("The message could not be deleted.");
      setPendingAction(null);
    }
  }

  return (
    <div className="admin-message-actions">
      <a className="admin-action-button primary" href={`mailto:${email}`}>
        <Mail aria-hidden />
        Reply by email
      </a>
      <button
        className="admin-action-button"
        type="button"
        onClick={toggleStatus}
        disabled={pendingAction !== null}
      >
        {pendingAction === "status" ? (
          <LoaderCircle className="admin-spinner" aria-hidden />
        ) : (
          <CheckCheck aria-hidden />
        )}
        {status === "read" ? "Mark as unread" : "Mark as read"}
      </button>
      <button
        className="admin-action-button danger"
        type="button"
        onClick={deleteMessage}
        disabled={pendingAction !== null}
      >
        {pendingAction === "delete" ? (
          <LoaderCircle className="admin-spinner" aria-hidden />
        ) : (
          <Trash2 aria-hidden />
        )}
        Delete
      </button>
      <p className="admin-action-error" role="alert">
        {error}
      </p>
    </div>
  );
}
