"use client";

import { Project } from "@/types/api";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function ProjectsTable({
  projects,
  token,
}: {
  projects: Project[];
  token: string;
}) {
  const router = useRouter();

  async function handleDelete(slug: string) {
    if (!window.confirm(`Supprimer "${slug}" ?`)) return;

    await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/admin/projects/${slug}`,
      {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    router.refresh();
  }

  return (
    <table>
      <thead>
        <th>#</th>
        <th>Titre</th>
        <th>Statut</th>
        <th></th>
        <th></th>
      </thead>
      <tbody>
        {projects.map((project) => (
          <tr key={project.slug}>
            <td>{project.slug}</td>
            <td>{project.title}</td>
            <td>{project.published}</td>
            <td>
              <Link href={`/admin/projects/${project.slug}/edit`}>
                <button>Editer</button>
              </Link>
            </td>
            <td>
              <button onClick={() => handleDelete(project.slug)}>
                Supprimer
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
