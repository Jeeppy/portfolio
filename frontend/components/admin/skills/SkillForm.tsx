"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { Skill } from "@/types/api";
import { useRouter } from "@/i18n/navigation";
import { useState } from "react";
import { Save } from "lucide-react";

export default function SkillForm({
  initialData,
  token,
}: {
  initialData?: Skill;
  token?: string;
}) {
  const router = useRouter();
  const [form, setForm] = useState({
    name: initialData?.name ?? "",
    category: initialData?.category ?? "",
    level: initialData?.level ?? 0,
  });
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();

    const method = initialData ? "PUT" : "POST";
    let url = `/api/admin/skills`;
    if (initialData) {
      url += `/${initialData.id}`;
    }
    try {
      await apiFetch(url, {
        method: method,
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(form),
      });
      router.push("/admin/skills");
    } catch (error) {
      if (error instanceof ApiError) {
        if (error.status === 409) setError("Cette compétence existe déjà.");
        else setError("Une erreur est survenue.");
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex max-w-lg flex-col gap-5">
      {error && <p className="text-sm text-red-500">{error}</p>}
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Libellé
        </label>
        <input
          name="name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Catégorie
        </label>
        <input
          name="category"
          value={form.category}
          onChange={(e) => setForm({ ...form, category: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Niveau
        </label>
        <input
          type="number"
          name="level"
          value={form.level}
          onChange={(e) => setForm({ ...form, level: Number(e.target.value) })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex justify-end">
        <button
          type="submit"
          className="flex items-center gap-2 rounded-md bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-indigo-500"
        >
          <Save size={16} />
          Enregistrer
        </button>
      </div>
    </form>
  );
}
