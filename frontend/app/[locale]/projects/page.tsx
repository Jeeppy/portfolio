import { apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import { Link } from "@/i18n/navigation";

export const dynamic = "force-dynamic";

export default async function ProjectsPage() {
  const projects = await apiFetch<Project[]>("/api/projects");
  const projectsItems = projects.map((project) => (
    <li key={project.id}>
      <Link href={`/projects/${project.slug}`}>
        {project.title} - {project.description}
      </Link>
    </li>
  ));
  return <ul>{projectsItems}</ul>;
}
