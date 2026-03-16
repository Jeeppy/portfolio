import { apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import ProjectsTable from "@/components/admin/projects/ProjectsTable";
import { Link } from "@/i18n/navigation";
import { Plus } from "lucide-react";
import { getToken } from "@/lib/auth";
import { adminFetch } from "@/lib/admin";
import { redirect } from "next/navigation";

export default async function AdminProjectsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const [token, { locale }] = await Promise.all([getToken(), params]);
  if (!token) redirect(`/${locale}/admin/login`);

  const projects = await adminFetch(
    () =>
      apiFetch<Project[]>("/api/admin/projects", {
        headers: { Authorization: `Bearer ${token}` },
      }),
    locale,
  );

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Projets</h1>
      <ProjectsTable projects={projects} token={token ?? ""} />
      <div className="mt-4 flex justify-end">
        <Link
          href="/admin/projects/new"
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500"
        >
          <Plus size={16} />
          Nouveau projet
        </Link>
      </div>
    </div>
  );
}
