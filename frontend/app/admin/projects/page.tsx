import { apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import { cookies } from "next/headers";
import ProjectsTable from "@/components/admin/projects/ProjectsTable";
import Link from "next/link";

export default async function AdminProjectsPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value;
  const projects = await apiFetch<Project[]>("/api/admin/projects", {
    headers: { Authorization: `Bearer ${token}` },
  });

  return (
    <div>
      <Link href="/admin/projects/new">
        <button>Nouveau projet</button>
      </Link>
      <ProjectsTable projects={projects} token={token ?? ""} />
    </div>
  );
}
