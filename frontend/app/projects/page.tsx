import { apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import Link from "next/link";

export const dynamic = "force-dynamic";

export default async function ListProjects() {
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
