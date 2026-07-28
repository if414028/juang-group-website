import fs from "node:fs/promises";
import path from "node:path";
import mysql from "mysql2/promise";

function getConnectionConfig() {
  if (process.env.DATABASE_URL) {
    const databaseUrl = new URL(process.env.DATABASE_URL);

    return {
      host: databaseUrl.hostname,
      port: Number(databaseUrl.port || 3306),
      user: decodeURIComponent(databaseUrl.username),
      password: decodeURIComponent(databaseUrl.password),
      database: decodeURIComponent(databaseUrl.pathname.replace(/^\//, "")),
    };
  }

  const required = ["DB_HOST", "DB_USER", "DB_NAME"];
  const missing = required.filter((key) => !process.env[key]);

  if (missing.length) {
    throw new Error(`Missing database variables: ${missing.join(", ")}`);
  }

  return {
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT || 3306),
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD || "",
    database: process.env.DB_NAME,
  };
}

const schemaPath = path.join(process.cwd(), "database", "schema.sql");
const schema = await fs.readFile(schemaPath, "utf8");
const connection = await mysql.createConnection({
  ...getConnectionConfig(),
  multipleStatements: true,
});

try {
  await connection.query(schema);
  console.log("Database tables are ready.");
} finally {
  await connection.end();
}
