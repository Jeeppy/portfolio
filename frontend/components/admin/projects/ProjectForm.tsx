"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import { useRouter } from "next/navigation";
import { useState } from "react";

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

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const token = document.cookie
      .split("; ")
      .find((c) => c.startsWith("token="))
      ?.split("=")[1];

    const method = initialData ? "PUT" : "POST";
    let url = `/api/admin/projects`;
    if (initialData) {
      url += `/${initialData.slug}`;
    }
    try {
      await apiFetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
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
    <form onSubmit={handleSubmit}>
      {error && <p>{error}</p>}
      <label>Titre</label>
      <input
        name="title"
        value={form.title}
        onChange={(e) => setForm({ ...form, title: e.target.value })}
      />
      <label>Slug</label>
      <input
        name="slug"
        value={form.slug}
        onChange={(e) => setForm({ ...form, slug: e.target.value })}
      />
      <label>Description</label>
      <textarea
        name="description"
        value={form.description}
        onChange={(e) => setForm({ ...form, description: e.target.value })}
      />
      <label>Adresse de démo</label>
      <input
        name="demo_url"
        value={form.demo_url}
        onChange={(e) => setForm({ ...form, demo_url: e.target.value })}
      />
      <label>Adresse du dépot</label>
      <input
        name="repository_url"
        value={form.repository_url}
        onChange={(e) => setForm({ ...form, repository_url: e.target.value })}
      />
      <label>Publié</label>
      <input
        type="radio"
        name="published"
        value="true"
        checked={form.published === true}
        onChange={() => setForm({ ...form, published: true })}
      />{" "}
      Oui
      <input
        type="radio"
        name="published"
        value="false"
        checked={form.published === false}
        onChange={() => setForm({ ...form, published: false })}
      />{" "}
      Non
      <button type="submit">Enregistrer</button>
    </form>
  );
}
