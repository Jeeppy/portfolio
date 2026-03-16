"use client";
import { Link, useRouter } from "@/i18n/navigation";
import { ApiError, apiFetch } from "@/lib/api";
import { Experience } from "@/types/api";
import { Pencil, Trash2 } from "lucide-react";
import { useState } from "react";

export default function ExperiencesTable({
  experiences,
  token,
}: {
  experiences: Experience[];
  token?: string;
}) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleDelete(experience: Experience) {
    if (!window.confirm(`Supprimer "${experience.company}" ?`)) return;

    try {
      await apiFetch(`/api/admin/experiences/${experience.id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      router.refresh();
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        setError("L'expérience n'existe pas.");
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
              <th className="px-4 py-3 font-medium">Société</th>
              <th className="px-4 py-3 font-medium">Localisation</th>
              <th className="px-4 py-3 font-medium">Poste</th>
              <th className="px-4 py-3 font-medium">Date de début</th>
              <th className="px-4 py-3 font-medium">Date de fin</th>
              <th className="px-4 py-3 text-right font-medium"></th>
            </tr>
          </thead>
          <tbody>
            {experiences.length === 0 ? (
              <tr>
                <td
                  colSpan={7}
                  className="px-4 py-8 text-center text-sm text-slate-400"
                >
                  Aucune expérience
                </td>
              </tr>
            ) : (
              experiences.map((experience) => (
                <tr
                  key={experience.id}
                  className="border-t border-slate-200 hover:bg-slate-100"
                >
                  <td className="px-4 py-3 text-slate-700">{experience.id}</td>
                  <td className="px-4 py-3 text-slate-700">
                    {experience.company}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {experience.location}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {experience.position}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {experience.start_date}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {experience.end_date}
                  </td>

                  <td className="px-4 py-3">
                    <div className="flex justify-end gap-2">
                      <Link
                        href={`/admin/experiences/${experience.id}/edit`}
                        className="rounded-md p-1.5 text-slate-400 transition-colors hover:bg-indigo-50 hover:text-indigo-600"
                      >
                        <Pencil size={15} />
                      </Link>
                      <button
                        onClick={() => handleDelete(experience)}
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
