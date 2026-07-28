import bcrypt from "bcryptjs";
import mysql from "mysql2/promise";

const email = process.env.ADMIN_EMAIL?.trim().toLowerCase();
const password = process.env.ADMIN_PASSWORD;
const name = process.env.ADMIN_NAME?.trim() || "Administrator";

if (!email || !password) {
  throw new Error("Set ADMIN_EMAIL and ADMIN_PASSWORD before creating an admin.");
}

if (password.length < 12) {
  throw new Error("ADMIN_PASSWORD must contain at least 12 characters.");
}

let connection;
if (process.env.DATABASE_URL) {
  connection = await mysql.createConnection(process.env.DATABASE_URL);
} else {
  connection = await mysql.createConnection({
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT || 3306),
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
  });
}

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
  console.log(`Admin account ready: ${email}`);
} finally {
  await connection.end();
}
