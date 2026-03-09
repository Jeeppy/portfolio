"use client";

import { Experience } from "@/types/api";
import { useRouter } from "@/i18n/navigation";
import { SyntheticEvent, useState } from "react";
import { Save } from "lucide-react";
import { ApiError, apiFetch } from "@/lib/api";

export default function ExperienceForm({
  initialData,
  token,
}: {
  initialData?: Experience;
  token?: string;
}) {
  const router = useRouter();
  const [form, setForm] = useState({
    company: initialData?.company ?? "",
    position: initialData?.position ?? "",
    location: initialData?.location ?? "",
    start_date: initialData?.start_date ?? "",
    end_date: initialData?.end_date ?? "",
    description: initialData?.description ?? "",
  });
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();

    const method = initialData ? "PUT" : "POST";
    let url = "/api/admin/experiences";
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
      router.push("/admin/experiences");
    } catch (error) {
      if (error instanceof ApiError) {
        setError("Une erreur est survenue.");
      } else {
        throw error;
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex max-w-lg flex-col gap-5">
      {error && <p className="text-sm text-red-500">{error}</p>}
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Entreprise
        </label>
        <input
          name="company"
          value={form.company}
          onChange={(e) => setForm({ ...form, company: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Poste
        </label>
        <input
          name="position"
          value={form.position}
          onChange={(e) => setForm({ ...form, position: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Localisation
        </label>
        <input
          name="location"
          value={form.location}
          onChange={(e) => setForm({ ...form, location: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex gap-4">
        <div className="flex flex-1 flex-col gap-1">
          <label className="block text-sm/6 font-semibold text-gray-700">
            Début
          </label>
          <input
            name="start_date"
            type="date"
            value={form.start_date}
            onChange={(e) => setForm({ ...form, start_date: e.target.value })}
            className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
          />
        </div>
        <div className="flex flex-1 flex-col gap-1">
          <label className="block text-sm/6 font-semibold text-gray-700">
            Fin
          </label>
          <input
            name="end_date"
            type="date"
            value={form.end_date}
            onChange={(e) => setForm({ ...form, end_date: e.target.value })}
            className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
          />
        </div>
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Description
        </label>
        <textarea
          name="description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          className="block h-32 w-full resize-none rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
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
