"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { Skill } from "@/types/api";
import { Link, useRouter } from "@/i18n/navigation";
import { useState } from "react";
import { Pencil, Trash2 } from "lucide-react";

export default function SkillsTable({
  skills,
  token,
}: {
  skills: Skill[];
  token?: string;
}) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleDelete(skill: Skill) {
    if (!window.confirm(`Supprimer "${skill.name}" ?`)) return;

    try {
      await apiFetch(`/api/admin/skills/${skill.id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      router.refresh();
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        setError("La compétence n'existe pas.");
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
          <thead className="bg-slate-100 text-xs tracking-wider text-slate-500 uppercase">
            <tr>
              <th className="px-4 py-3 font-medium">#</th>
              <th className="px-4 py-3 font-medium">Libellé</th>
              <th className="px-4 py-3 font-medium">Catégorie</th>
              <th className="px-4 py-3 font-medium">Niveau</th>
              <th className="px-4 py-3 text-right font-medium"></th>
            </tr>
          </thead>
          <tbody>
            {skills.length === 0 ? (
              <tr>
                <td
                  colSpan={5}
                  className="px-4 py-8 text-center text-sm text-slate-400"
                >
                  Aucune compétence
                </td>
              </tr>
            ) : (
              skills.map((skill) => (
                <tr
                  key={skill.id}
                  className="border-t border-slate-200 hover:bg-slate-100"
                >
                  <td className="px-4 py-3 text-slate-700">{skill.id}</td>
                  <td className="px-4 py-3 text-slate-700">{skill.name}</td>
                  <td className="px-4 py-3 text-slate-700">{skill.category}</td>
                  <td className="px-4 py-3 text-slate-700">{skill.level}</td>
                  <td className="px-4 py-3">
                    <div className="flex justify-end gap-2">
                      <Link
                        href={`/admin/skills/${skill.id}/edit`}
                        className="rounded-md p-1.5 text-slate-400 transition-colors hover:bg-indigo-50 hover:text-indigo-600"
                      >
                        <Pencil size={15} />
                      </Link>
                      <button
                        onClick={() => handleDelete(skill)}
                        className="rounded-md p-1.5 text-slate-400 transition-colors hover:bg-red-50 hover:text-red-600"
                      >
                        <Trash2 size={15} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
