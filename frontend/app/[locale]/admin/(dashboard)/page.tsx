import { Link } from "@/i18n/navigation";
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

export default async function AdminPage() {
  const token = await getToken();
  const [projects, skills, experiences, education, messages] =
    await Promise.all([
      apiFetch<Project[]>("/api/admin/projects", {
        headers: { Authorization: `Bearer ${token}` },
      }),
      apiFetch<Skill[]>("/api/skills"),
      apiFetch<Experience[]>("/api/experiences"),
      apiFetch<Education[]>("/api/education"),
      apiFetch<ContactMessage[]>("/api/admin/contact", {
        headers: { Authorization: `Bearer ${token}` },
      }),
    ]);
  const unread = messages
    .filter((m) => !m.read)
    .sort(
      (a, b) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
    );

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800">Dashboard</h1>
      <div className="mt-8 grid grid-cols-2 gap-4 px-4 py-4 sm:px-8 lg:grid-cols-4">
        <div className="flex items-center overflow-hidden rounded-xl bg-white shadow-md">
          <div className="flex items-center self-stretch bg-green-400 p-4 text-white">
            <FolderOpen size={22} />
          </div>
          <div className="px-4 py-4 text-gray-700">
            <h3 className="text-xs font-medium tracking-widest text-gray-500 uppercase">
              Projets
            </h3>
            <p className="text-3xl font-bold">{projects.length}</p>
          </div>
        </div>
        <div className="flex items-center overflow-hidden rounded-xl bg-white shadow-md">
          <div className="flex items-center self-stretch bg-blue-400 p-4 text-white">
            <Wrench size={22} />
          </div>
          <div className="px-4 py-4 text-gray-700">
            <h3 className="text-xs font-medium tracking-widest text-gray-500 uppercase">
              Compétences
            </h3>
            <p className="text-3xl font-bold">{skills.length}</p>
          </div>
        </div>
        <div className="flex items-center overflow-hidden rounded-xl bg-white shadow-md">
          <div className="flex items-center self-stretch bg-violet-400 p-4 text-white">
            <Briefcase size={22} />
          </div>
          <div className="px-4 py-4 text-gray-700">
            <h3 className="text-xs font-medium tracking-widest text-gray-500 uppercase">
              Experiences
            </h3>
            <p className="text-3xl font-bold">{experiences.length}</p>
          </div>
        </div>
        <div className="flex items-center overflow-hidden rounded-xl bg-white shadow-md">
          <div className="flex items-center self-stretch bg-amber-400 p-4 text-white">
            <GraduationCap size={22} />
          </div>
          <div className="px-4 py-4 text-gray-700">
            <h3 className="text-xs font-medium tracking-widest text-gray-500 uppercase">
              Formations
            </h3>
            <p className="text-3xl font-bold">{education.length}</p>
          </div>
        </div>
      </div>
      <div className="mt-6">
        <h2 className="mb-3 text-lg font-semibold text-slate-800">
          Messages non lus{" "}
          <span className="ml-1 rounded-full bg-red-100 px-2 py-0.5 text-sm text-red-600">
            {unread.length}
          </span>
        </h2>
        <div className="rounded-xl border bg-white shadow-sm"></div>
        {unread.length === 0 ? (
          <p className="p-6 text-sm text-slate-400">Aucun message non lu.</p>
        ) : (
          <ul className="divide-y divide-slate-100">
            {unread.map((message) => (
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
  );
}
