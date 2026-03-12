import { Link } from "@/i18n/navigation";
import LogoutButton from "@/components/admin/LogoutButton";
import { ReactNode } from "react";
import {
  Briefcase,
  FolderKanban,
  GraduationCap,
  LayoutDashboard,
  MessageSquare,
  User,
  Wrench,
} from "lucide-react";

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
            className="flex gap-2 rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            <LayoutDashboard size={16} />
            Dashboard
          </Link>
          <Link
            href="/admin/profile"
            className="flex gap-2 rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            <User size={16} />
            Profile
          </Link>
          <Link
            href="/admin/projects"
            className="flex gap-2 rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            <FolderKanban size={16} />
            Projets
          </Link>
          <Link
            href="/admin/skills"
            className="flex gap-2 rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            <Wrench size={16} />
            Compétences
          </Link>
          <Link
            href="/admin/experiences"
            className="flex gap-2 rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            <Briefcase size={16} />
            Expériences
          </Link>
          <Link
            href="/admin/education"
            className="flex gap-2 rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            <GraduationCap size={16} />
            Formations
          </Link>
          <Link
            href="/admin/contact"
            className="flex gap-2 rounded-lg px-3 py-2 text-sm hover:bg-slate-700"
          >
            <MessageSquare size={16} />
            Messages
          </Link>
          <LogoutButton />
        </nav>
      </aside>
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}
