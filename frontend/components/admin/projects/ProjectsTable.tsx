"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import { Link, useRouter } from "@/i18n/navigation";
import { useState } from "react";

export default function ProjectsTable({
  projects,
  token,
}: {
  projects: Project[];
  token: string;
}) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleDelete(slug: string) {
    if (!window.confirm(`Supprimer "${slug}" ?`)) return;

    try {
      await apiFetch(`/api/admin/projects/${slug}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      router.refresh();
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        setError("Le projet n'existe pas.");
      } else {
        throw error;
      }
    }
  }

  return (
    <div>
      {error && <p>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Titre</th>
            <th>Statut</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project) => (
            <tr key={project.slug}>
              <td>{project.slug}</td>
              <td>{project.title}</td>
              <td>{project.published ? "Publié" : "Brouillon"}</td>
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
    </div>
  );
}
