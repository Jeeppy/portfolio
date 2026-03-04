"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { Skill } from "@/types/api";
import { Link, useRouter } from "@/i18n/navigation";
import { useState } from "react";

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
    if (!window.confirm(`Supprimer "${skill.name}"`)) return;

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
      {error && <p>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Libellé</th>
            <th>Catégorie</th>
            <th>Niveau</th>
          </tr>
        </thead>
        <tbody>
          {skills.map((skill) => (
            <tr key={skill.id}>
              <td>{skill.id}</td>
              <td>{skill.name}</td>
              <td>{skill.category}</td>
              <td>{skill.level}</td>
              <td>
                <Link href={`/admin/skills/${skill.id}/edit`}>
                  <button>Editer</button>
                </Link>
              </td>
              <td>
                <button onClick={() => handleDelete(skill)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
