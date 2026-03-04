"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { getClientToken } from "@/lib/auth";
import { Skill } from "@/types/api";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function SkillForm({ initialData }: { initialData?: Skill }) {
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
          Authorization: `Bearer ${getClientToken()}`,
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
    <form onSubmit={handleSubmit}>
      {error && <p>{error}</p>}
      <label>Libellé</label>
      <input
        name="name"
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
      />
      <label>Catégorie</label>
      <input
        name="category"
        value={form.category}
        onChange={(e) => setForm({ ...form, category: e.target.value })}
      />
      <label>Niveau</label>
      <input
        type="number"
        name="level"
        value={form.level}
        onChange={(e) => setForm({ ...form, level: Number(e.target.value) })}
      />
      <button type="submit">Enregistrer</button>
    </form>
  );
}
