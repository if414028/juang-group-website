import "server-only";

import mysql, { type Pool } from "mysql2/promise";

declare global {
  var juangDatabasePool: Pool | undefined;
}

function createDatabasePool() {
  if (process.env.DATABASE_URL) {
    const databaseUrl = new URL(process.env.DATABASE_URL);

    if (!["mysql:", "mysql2:"].includes(databaseUrl.protocol)) {
      throw new Error("DATABASE_URL must use the mysql:// protocol.");
    }

    return mysql.createPool({
      host: databaseUrl.hostname,
      port: Number(databaseUrl.port || 3306),
      user: decodeURIComponent(databaseUrl.username),
      password: decodeURIComponent(databaseUrl.password),
      database: decodeURIComponent(databaseUrl.pathname.replace(/^\//, "")),
      connectionLimit: 8,
      enableKeepAlive: true,
      keepAliveInitialDelay: 0,
      timezone: "Z",
      ssl:
        process.env.DB_SSL === "true"
          ? { rejectUnauthorized: process.env.DB_SSL_REJECT_UNAUTHORIZED !== "false" }
          : undefined,
    });
  }

  const host = process.env.DB_HOST;
  const user = process.env.DB_USER;
  const database = process.env.DB_NAME;

  if (!host || !user || !database) {
    throw new Error(
      "MySQL is not configured. Set DATABASE_URL or DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME.",
    );
  }

  return mysql.createPool({
    host,
    port: Number(process.env.DB_PORT || 3306),
    user,
    password: process.env.DB_PASSWORD,
    database,
    connectionLimit: 8,
    enableKeepAlive: true,
    keepAliveInitialDelay: 0,
    timezone: "Z",
    ssl:
      process.env.DB_SSL === "true"
        ? { rejectUnauthorized: process.env.DB_SSL_REJECT_UNAUTHORIZED !== "false" }
        : undefined,
  });
}

export function getDatabase() {
  if (!globalThis.juangDatabasePool) {
    globalThis.juangDatabasePool = createDatabasePool();
  }

  return globalThis.juangDatabasePool;
}
