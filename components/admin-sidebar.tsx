"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Inbox,
  LogOut,
  Menu,
  Settings,
  ShieldCheck,
  UserRound,
  X,
} from "lucide-react";

export function AdminSidebar({ email }: { email: string }) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    if (open) closeButtonRef.current?.focus();

    function handleEscape(event: KeyboardEvent) {
      if (event.key === "Escape") setOpen(false);
    }

    document.addEventListener("keydown", handleEscape);
    return () => {
      document.body.style.overflow = "";
      document.removeEventListener("keydown", handleEscape);
    };
  }, [open]);

  return (
    <>
      <header className="admin-mobile-bar">
        <Link
          className="admin-mobile-brand"
          href="/admin"
          onClick={() => setOpen(false)}
        >
          <span className="admin-logo" aria-hidden />
          <span>
            <strong>Juang Group</strong>
            <small>Admin Dashboard</small>
          </span>
        </Link>
        <button
          type="button"
          aria-label="Open navigation"
          aria-controls="admin-sidebar"
          aria-expanded={open}
          onClick={() => setOpen(true)}
        >
          <Menu aria-hidden />
        </button>
      </header>

      <button
        className="admin-sidebar-overlay"
        data-open={open}
        type="button"
        aria-label="Close navigation"
        tabIndex={open ? 0 : -1}
        onClick={() => setOpen(false)}
      />

      <aside
        className="admin-sidebar"
        id="admin-sidebar"
        data-open={open}
        aria-label="Admin navigation"
      >
        <div className="admin-sidebar-heading">
          <Link
            className="admin-sidebar-brand"
            href="/admin"
            onClick={() => setOpen(false)}
          >
            <span className="admin-logo" aria-hidden />
            <span>
              <strong>Juang Group</strong>
              <small>Admin Dashboard</small>
            </span>
          </Link>
          <button
            ref={closeButtonRef}
            className="admin-sidebar-close"
            type="button"
            aria-label="Close navigation"
            onClick={() => setOpen(false)}
          >
            <X aria-hidden />
          </button>
        </div>

        <nav>
          <p>Workspace</p>
          <Link
            className={pathname === "/admin" ? "active" : ""}
            href="/admin"
            aria-current={pathname === "/admin" ? "page" : undefined}
            onClick={() => setOpen(false)}
          >
            <Inbox aria-hidden />
            Inbox
          </Link>

          <p className="admin-nav-group">
            <Settings aria-hidden />
            Settings
          </p>
          <Link
            className={`admin-subnav-link ${
              pathname.startsWith("/admin/settings/profile") ? "active" : ""
            }`}
            href="/admin/settings/profile"
            aria-current={
              pathname.startsWith("/admin/settings/profile")
                ? "page"
                : undefined
            }
            onClick={() => setOpen(false)}
          >
            <UserRound aria-hidden />
            Profile
          </Link>
        </nav>

        <div className="admin-sidebar-footer">
          <p>
            <ShieldCheck aria-hidden />
            <span>
              <small>Signed in as</small>
              <strong>{email}</strong>
            </span>
          </p>
          <form action="/api/admin/logout" method="post">
            <button type="submit">
              <LogOut aria-hidden />
              Sign out
            </button>
          </form>
        </div>
      </aside>
    </>
  );
}
