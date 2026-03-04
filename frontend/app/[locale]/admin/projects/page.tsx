import { ApiError, apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import { cookies } from "next/headers";
import ProjectsTable from "@/components/admin/projects/ProjectsTable";
import { Link } from "@/i18n/navigation";
import { redirect } from "next/navigation";

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
      <Link href="/admin/projects/new">
        <button>Nouveau projet</button>
      </Link>
      <ProjectsTable projects={projects} token={token ?? ""} />
    </div>
  );
}
