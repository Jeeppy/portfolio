import { ApiError, apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import ProjectsTable from "@/components/admin/projects/ProjectsTable";
import { Link } from "@/i18n/navigation";
import { redirect } from "next/navigation";
import { Plus } from "lucide-react";
import { getToken } from "@/lib/auth";

export default async function AdminProjectsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const token = await getToken();
  let projects: Project[] | undefined = undefined;
  try {
    projects = await apiFetch<Project[]>("/api/admin/projects", {
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      const { locale } = await params;
      return redirect(`/${locale}/admin/login`);
    } else {
      throw error;
    }
  }

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
