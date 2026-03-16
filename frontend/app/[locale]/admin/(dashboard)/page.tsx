import StatCard from "@/components/admin/StatCard";
import { Link } from "@/i18n/navigation";
import { adminFetch } from "@/lib/admin";
import { apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import {
  ContactMessage,
  Education,
  Experience,
  Project,
  Skill,
} from "@/types/api";
import { Briefcase, FolderOpen, GraduationCap, Wrench } from "lucide-react";
import { redirect } from "next/navigation";

export default async function AdminPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const token = await getToken();
  const { locale } = await params;
  if (!token) redirect(`/${locale}/admin/login`);

  const [projects, skills, experiences, education, messages] =
    await Promise.all([
      adminFetch(
        () =>
          apiFetch<Project[]>("/api/admin/projects", {
            headers: { Authorization: `Bearer ${token}` },
          }),
        locale,
      ),
      adminFetch(() => apiFetch<Skill[]>("/api/skills"), locale),
      adminFetch(() => apiFetch<Experience[]>("/api/experiences"), locale),
      adminFetch(() => apiFetch<Education[]>("/api/education"), locale),
      adminFetch(
        () =>
          apiFetch<ContactMessage[]>("/api/admin/contact?read=false", {
            headers: { Authorization: `Bearer ${token}` },
          }),
        locale,
      ),
    ]);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800">Dashboard</h1>
      <div className="mt-8 grid grid-cols-2 gap-4 px-4 py-4 sm:px-8 lg:grid-cols-4">
        <StatCard
          Icon={FolderOpen}
          color="bg-green-400"
          label="Projets"
          count={projects.length}
        />
        <StatCard
          Icon={Wrench}
          color="bg-blue-400"
          label="Compétences"
          count={skills.length}
        />
        <StatCard
          Icon={Briefcase}
          color="bg-violet-400"
          label="Expériences"
          count={experiences.length}
        />
        <StatCard
          Icon={GraduationCap}
          color="bg-amber-400"
          label="Formations"
          count={education.length}
        />
      </div>
      <div className="mt-6">
        <h2 className="mb-3 text-lg font-semibold text-slate-800">
          Messages non lus{" "}
          <span className="ml-1 rounded-full bg-red-100 px-2 py-0.5 text-sm text-red-600">
            {messages.length}
          </span>
        </h2>
        <div className="rounded-xl bg-white shadow-md">
          {messages.length === 0 ? (
            <p className="p-6 text-sm text-slate-400">Aucun message non lu.</p>
          ) : (
            <ul className="divide-y divide-slate-100">
              {messages.map((message) => (
                <li key={message.id}>
                  <Link
                    href="/admin/contact"
                    className="flex items-center justify-between px-6 py-4"
                  >
                    <div>
                      <p className="text-sm font-medium text-slate-800">
                        {message.subject}
                      </p>
                      <p className="text-xs text-slate-400">
                        {message.name} · {message.email}
                      </p>
                    </div>
                    <span className="text-xs text-slate-400">
                      {new Date(message.created_at).toLocaleDateString("fr-FR")}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
