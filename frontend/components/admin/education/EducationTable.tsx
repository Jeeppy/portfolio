"use client";
import { Link, useRouter } from "@/i18n/navigation";
import { ApiError, apiFetch } from "@/lib/api";
import { Education } from "@/types/api";
import { Check, Minus, Pencil, Trash2 } from "lucide-react";
import { useState } from "react";

export default function EducationTable({
  educations,
  token,
}: {
  educations: Education[];
  token?: string;
}) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleDelete(education: Education) {
    if (!window.confirm(`Supprimer "${education.school}" ?`)) return;

    try {
      await apiFetch(`/api/admin/education/${education.id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      router.refresh();
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        setError("La formation n'existe pas.");
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
              <th className="px-4 py-3 font-medium">École</th>
              <th className="px-4 py-3 font-medium">Diplôme</th>
              <th className="px-4 py-3 font-medium">Lieu</th>
              <th className="px-4 py-3 font-medium">Année</th>
              <th className="px-4 py-3 font-medium">Alternance</th>
              <th className="px-4 py-3 text-right font-medium"></th>
            </tr>
          </thead>
          <tbody>
            {educations.map((education) => (
              <tr
                key={education.id}
                className="border-t border-slate-200 hover:bg-slate-100"
              >
                <td className="px-4 py-3 text-slate-700">{education.id}</td>
                <td className="px-4 py-3 text-slate-700">{education.school}</td>
                <td className="px-4 py-3 text-slate-700">{education.degree}</td>
                <td className="px-4 py-3 text-slate-700">
                  {education.location}
                </td>
                <td className="px-4 py-3 text-slate-700">{education.year}</td>
                <td className="px-4 py-3 text-slate-700">
                  {education.is_alternance ? (
                    <Check size={15} />
                  ) : (
                    <Minus size={15} />
                  )}
                </td>

                <td className="px-4 py-3">
                  <div className="flex justify-end gap-2">
                    <Link
                      href={`/admin/education/${education.id}/edit`}
                      className="rounded-md p-1.5 text-slate-400 transition-colors hover:bg-indigo-50 hover:text-indigo-600"
                    >
                      <Pencil size={15} />
                    </Link>
                    <button
                      onClick={() => handleDelete(education)}
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
