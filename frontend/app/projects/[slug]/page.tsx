import { apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import Link from "next/link";
import { cache } from "react";

export const dynamic = "force-dynamic";

const getProject = cache((slug: string) =>
  apiFetch<Project>(`/api/projects/${slug}`),
);

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const project = await getProject(slug);
  return {
    title: project.title,
    description: project.description ?? undefined,
  };
}

export default async function ProjectPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const project = await getProject(slug);

  return (
    <main>
      <h1>{project.title}</h1>
      <p>{project.description}</p>
      <ul>
        {project.repository_url && (
          <li>
            <Link href={project.repository_url}>Dépot</Link>
          </li>
        )}
        {project.demo_url && (
          <li>
            <Link href={project.demo_url}>Démo</Link>
          </li>
        )}
      </ul>
    </main>
  );
}
