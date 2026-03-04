import { ApiError, apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import { cookies } from "next/headers";
import ProjectsTable from "@/components/admin/projects/ProjectsTable";
import Link from "next/link";
import { redirect } from "next/navigation";

export default async function AdminProjectsPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value;
  let projects: Project[] | undefined = undefined;
  try {
    projects = await apiFetch<Project[]>("/api/admin/projects", {
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      return redirect("/admin/login");
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
