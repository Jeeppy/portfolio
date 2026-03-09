import { Link } from "@/i18n/navigation";
import LogoutButton from "@/components/admin/LogoutButton";
import { ReactNode } from "react";

export default function DashboardLayout({
  children,
}: Readonly<{ children: ReactNode }>) {
  return (
    <div className="flex min-h-screen bg-slate-50">
      <aside className="flex w-56 flex-col gap-2 bg-slate-900 p-4 text-slate-100">
        <p className="mb-2 text-xs font-semibold tracking-widest text-slate-400 uppercase">
          Admin
        </p>
        <nav className="flex flex-1 flex-col gap-1">
          <Link
            href="/admin"
            className="rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            Dashboard
          </Link>
          <Link
            href="/admin/projects"
            className="rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            Projets
          </Link>
          <Link
            href="/admin/skills"
            className="rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            Compétences
          </Link>
        </nav>
        <LogoutButton />
      </aside>
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}
