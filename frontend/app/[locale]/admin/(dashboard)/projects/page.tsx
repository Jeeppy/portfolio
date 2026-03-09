import { ApiError, apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import { cookies } from "next/headers";
import ProjectsTable from "@/components/admin/projects/ProjectsTable";
import { Link } from "@/i18n/navigation";
import { redirect } from "next/navigation";
import { Plus } from "lucide-react";

export default async function AdminProjectsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value;
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
        <Link href="/admin/projects/new">
          <button className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500">
            <Plus size={16} />
            Nouveau projet
          </button>
        </Link>
      </div>
    </div>
  );
}
