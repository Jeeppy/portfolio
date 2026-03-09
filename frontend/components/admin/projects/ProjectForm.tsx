"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { getClientToken } from "@/lib/auth.client";
import { Project } from "@/types/api";
import { useRouter } from "@/i18n/navigation";
import { useState } from "react";
import { Save } from "lucide-react";

export default function ProjectForm({
  initialData,
}: {
  initialData?: Project;
}) {
  const router = useRouter();

  const [form, setForm] = useState({
    title: initialData?.title ?? "",
    slug: initialData?.slug ?? "",
    description: initialData?.description ?? "",
    demo_url: initialData?.demo_url ?? "",
    repository_url: initialData?.repository_url ?? "",
    published: initialData?.published ?? true,
  });
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();

    const method = initialData ? "PUT" : "POST";
    let url = `/api/admin/projects`;
    if (initialData) {
      url += `/${initialData.slug}`;
    }
    try {
      await apiFetch(url, {
        method: method,
        headers: {
          Authorization: `Bearer ${getClientToken()}`,
        },
        body: JSON.stringify(form),
      });
      router.push("/admin/projects");
    } catch (error) {
      if (error instanceof ApiError) {
        if (error.status === 409) setError("Ce slug existe déjà.");
        else setError("Une erreur est survenue.");
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex max-w-lg flex-col gap-5">
      {error && <p className="text-sm text-red-500">{error}</p>}

      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Titre
        </label>
        <input
          name="title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Slug
        </label>
        <input
          name="slug"
          value={form.slug}
          onChange={(e) => setForm({ ...form, slug: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
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
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Adresse de démo
        </label>
        <input
          name="demo_url"
          value={form.demo_url}
          onChange={(e) => setForm({ ...form, demo_url: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Adresse du dépot
        </label>
        <input
          name="repository_url"
          value={form.repository_url}
          onChange={(e) => setForm({ ...form, repository_url: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Publié
        </label>
        <div className="flex gap-4 text-sm text-slate-700">
          <label className="flex items-center gap-2">
            <input
              type="radio"
              name="published"
              value="true"
              checked={form.published === true}
              onChange={() => setForm({ ...form, published: true })}
            />{" "}
            Oui
          </label>
          <label className="flex items-center gap-2">
            <input
              type="radio"
              name="published"
              value="false"
              checked={form.published === false}
              onChange={() => setForm({ ...form, published: false })}
            />{" "}
            Non
          </label>
        </div>
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
