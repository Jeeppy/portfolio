"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import { Link, useRouter } from "@/i18n/navigation";
import { useState } from "react";
import { Pencil, Trash2 } from "lucide-react";

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
      {error && <p className="mb-4 text-sm text-red-500">{error}</p>}
      <div className="overflow-x-auto rounded-lg border border-slate-200">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="bg-slate-100 text-xs tracking-wider text-slate-500 uppercase">
              <th className="px-4 py-3 font-medium">#</th>
              <th className="px-4 py-3 font-medium">Titre</th>
              <th className="px-4 py-3 font-medium">Statut</th>
              <th className="px-4 py-3 text-right font-medium"></th>
            </tr>
          </thead>
          <tbody>
            {projects.map((project) => (
              <tr
                key={project.slug}
                className="border-t border-slate-200 hover:bg-slate-100"
              >
                <td className="px-4 py-3 text-slate-700">{project.slug}</td>
                <td className="px-4 py-3 text-slate-700">{project.title}</td>
                <td className="px-4 py-3 text-slate-700">
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                      project.published
                        ? "bg-green-100 text-green-700"
                        : "bg-slate-100 text-slate-500"
                    }`}
                  >
                    {project.published ? "Publié" : "Brouillon"}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex justify-end gap-2">
                    <Link
                      href={`/admin/projects/${project.slug}/edit`}
                      className="rounded-md p-1.5 text-slate-400 transition-colors hover:bg-indigo-50 hover:text-indigo-600"
                    >
                      <Pencil size={15} />
                    </Link>
                    <button
                      onClick={() => handleDelete(project.slug)}
                      className="rounded-md p-1.5 text-slate-400 transition-colors hover:bg-red-50 hover:text-red-600"
                    >
                      <Trash2 size={15} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
