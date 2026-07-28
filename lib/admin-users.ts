import "server-only";

import type { ResultSetHeader, RowDataPacket } from "mysql2";
import { getDatabase } from "@/lib/db";

export type AdminUser = {
  id: number;
  email: string;
  passwordHash: string;
  name: string;
  isActive: boolean;
};

type AdminUserRow = RowDataPacket & {
  id: number;
  email: string;
  password_hash: string;
  name: string;
  is_active: number;
};

export async function getAdminByEmail(email: string) {
  const database = getDatabase();
  const [rows] = await database.execute<AdminUserRow[]>(
    `SELECT id, email, password_hash, name, is_active
     FROM admin_users
     WHERE email = ?
     LIMIT 1`,
    [email],
  );

  const row = rows[0];
  if (!row) return null;

  return {
    id: Number(row.id),
    email: row.email,
    passwordHash: row.password_hash,
    name: row.name,
    isActive: Boolean(row.is_active),
  } satisfies AdminUser;
}

export async function getAdminById(id: number) {
  const database = getDatabase();
  const [rows] = await database.execute<AdminUserRow[]>(
    `SELECT id, email, password_hash, name, is_active
     FROM admin_users
     WHERE id = ?
     LIMIT 1`,
    [id],
  );

  const row = rows[0];
  if (!row) return null;

  return {
    id: Number(row.id),
    email: row.email,
    passwordHash: row.password_hash,
    name: row.name,
    isActive: Boolean(row.is_active),
  } satisfies AdminUser;
}

export async function updateAdminProfile(input: {
  id: number;
  name: string;
  email: string;
  passwordHash?: string;
}) {
  const database = getDatabase();

  if (input.passwordHash) {
    await database.execute<ResultSetHeader>(
      `UPDATE admin_users
       SET name = ?, email = ?, password_hash = ?
       WHERE id = ?`,
      [input.name, input.email, input.passwordHash, input.id],
    );
    return;
  }

  await database.execute<ResultSetHeader>(
    `UPDATE admin_users
     SET name = ?, email = ?
     WHERE id = ?`,
    [input.name, input.email, input.id],
  );
}

export async function updateAdminLastLogin(id: number) {
  const database = getDatabase();
  await database.execute<ResultSetHeader>(
    "UPDATE admin_users SET last_login_at = UTC_TIMESTAMP() WHERE id = ?",
    [id],
  );
}
