"use client";

import { Education } from "@/types/api";
import { useRouter } from "@/i18n/navigation";
import { SyntheticEvent, useState } from "react";
import { Save } from "lucide-react";
import { ApiError, apiFetch } from "@/lib/api";

export default function EducationForm({
  initialData,
  token,
}: {
  initialData?: Education;
  token?: string;
}) {
  const router = useRouter();
  const [form, setForm] = useState({
    school: initialData?.school ?? "",
    degree: initialData?.degree ?? "",
    location: initialData?.location ?? "",
    year: initialData?.year ?? new Date().getFullYear(),
    is_alternance: initialData?.is_alternance ?? false,
  });
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();

    const method = initialData ? "PUT" : "POST";
    let url = "/api/admin/education";
    if (initialData) {
      url += `/${initialData.id}`;
    }
    try {
      await apiFetch(url, {
        method: method,
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...form,
          location: form.location || null,
        }),
      });
      router.push("/admin/education");
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
          École
        </label>
        <input
          name="school"
          value={form.school}
          onChange={(e) => setForm({ ...form, school: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Diplôme
        </label>
        <input
          name="degree"
          value={form.degree}
          onChange={(e) => setForm({ ...form, degree: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Lieu
        </label>
        <input
          name="location"
          value={form.location}
          onChange={(e) => setForm({ ...form, location: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Année
        </label>
        <input
          name="year"
          type="number"
          value={form.year}
          onChange={(e) => setForm({ ...form, year: Number(e.target.value) })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="flex cursor-pointer items-center gap-2 text-sm/6 font-semibold text-gray-700">
          <input
            name="is_alternance"
            type="checkbox"
            checked={form.is_alternance}
            onChange={(e) =>
              setForm({ ...form, is_alternance: e.target.checked })
            }
            className="h-4 w-4 rounded border-gray-400 accent-indigo-600"
          />
          En alternance
        </label>
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
