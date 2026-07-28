import bcrypt from "bcryptjs";
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

const email = process.env.ADMIN_EMAIL?.trim().toLowerCase();
const password = process.env.ADMIN_PASSWORD;
const name = process.env.ADMIN_NAME?.trim() || "Website Admin";

if (!email || !password) {
  throw new Error("Set ADMIN_EMAIL and ADMIN_PASSWORD before running the seeder.");
}

if (password.length < 12) {
  throw new Error("ADMIN_PASSWORD must contain at least 12 characters.");
}

const connection = await mysql.createConnection(getConnectionConfig());

try {
  const passwordHash = await bcrypt.hash(password, 12);

  await connection.execute(
    `INSERT INTO admin_users (email, password_hash, name, is_active)
     VALUES (?, ?, ?, TRUE)
     ON DUPLICATE KEY UPDATE
       password_hash = VALUES(password_hash),
       name = VALUES(name),
       is_active = TRUE`,
    [email, passwordHash, name],
  );

  console.log(`Seed completed. Admin account ready: ${email}`);
} finally {
  await connection.end();
}
