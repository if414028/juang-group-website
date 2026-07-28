import "server-only";

import type { ResultSetHeader, RowDataPacket } from "mysql2";
import { getDatabase } from "@/lib/db";

export type MessageStatus = "unread" | "read";

export type ContactMessage = {
  id: number;
  name: string;
  email: string;
  subject: string;
  message: string;
  status: MessageStatus;
  readAt: Date | null;
  createdAt: Date;
};

type ContactMessageRow = RowDataPacket & {
  id: number;
  name: string;
  email: string;
  subject: string;
  message: string;
  status: MessageStatus;
  read_at: Date | null;
  created_at: Date;
};

function mapMessage(row: ContactMessageRow): ContactMessage {
  return {
    id: Number(row.id),
    name: row.name,
    email: row.email,
    subject: row.subject,
    message: row.message,
    status: row.status,
    readAt: row.read_at ? new Date(row.read_at) : null,
    createdAt: new Date(row.created_at),
  };
}

export async function createContactMessage(input: {
  name: string;
  email: string;
  subject: string;
  message: string;
  ipAddress: string | null;
  userAgent: string | null;
}) {
  const database = getDatabase();
  const [result] = await database.execute<ResultSetHeader>(
    `INSERT INTO contact_messages
      (name, email, subject, message, status, ip_address, user_agent)
     VALUES (?, ?, ?, ?, 'unread', ?, ?)`,
    [
      input.name,
      input.email,
      input.subject,
      input.message,
      input.ipAddress,
      input.userAgent,
    ],
  );

  return result.insertId;
}

export async function getMessageCounts() {
  const database = getDatabase();
  const [rows] = await database.query<
    (RowDataPacket & { total: number; unread: number; read_count: number })[]
  >(
    `SELECT
      COUNT(*) AS total,
      SUM(status = 'unread') AS unread,
      SUM(status = 'read') AS read_count
     FROM contact_messages`,
  );

  const counts = rows[0];
  return {
    total: Number(counts?.total || 0),
    unread: Number(counts?.unread || 0),
    read: Number(counts?.read_count || 0),
  };
}

export async function listContactMessages(options: {
  status?: MessageStatus | "all";
  query?: string;
  limit?: number;
}) {
  const database = getDatabase();
  const where: string[] = [];
  const values: Array<string | number> = [];

  if (options.status && options.status !== "all") {
    where.push("status = ?");
    values.push(options.status);
  }

  if (options.query) {
    where.push("(name LIKE ? OR email LIKE ? OR subject LIKE ? OR message LIKE ?)");
    const term = `%${options.query}%`;
    values.push(term, term, term, term);
  }

  const limit = Math.min(Math.max(options.limit || 100, 1), 200);

  const [rows] = await database.execute<ContactMessageRow[]>(
    `SELECT id, name, email, subject, message, status, read_at, created_at
     FROM contact_messages
     ${where.length ? `WHERE ${where.join(" AND ")}` : ""}
     ORDER BY created_at DESC
     LIMIT ${limit}`,
    values,
  );

  return rows.map(mapMessage);
}

export async function getContactMessage(id: number) {
  const database = getDatabase();
  const [rows] = await database.execute<ContactMessageRow[]>(
    `SELECT id, name, email, subject, message, status, read_at, created_at
     FROM contact_messages
     WHERE id = ?
     LIMIT 1`,
    [id],
  );

  return rows[0] ? mapMessage(rows[0]) : null;
}

export async function setMessageStatus(id: number, status: MessageStatus) {
  const database = getDatabase();
  const [result] = await database.execute<ResultSetHeader>(
    `UPDATE contact_messages
     SET status = ?, read_at = ${status === "read" ? "COALESCE(read_at, UTC_TIMESTAMP())" : "NULL"}
     WHERE id = ?`,
    [status, id],
  );

  return result.affectedRows > 0;
}

export async function deleteContactMessage(id: number) {
  const database = getDatabase();
  const [result] = await database.execute<ResultSetHeader>(
    "DELETE FROM contact_messages WHERE id = ?",
    [id],
  );

  return result.affectedRows > 0;
}
