import { apiFetch } from "@/lib/api";
import { Profile } from "@/types/api";

export const dynamic = "force-dynamic";

export default async function SkillsPage() {
  const profile = await apiFetch<Profile>("/api/profile");
  const skills = profile.skills;
  const groupedSkills = skills.reduce<Record<string, typeof skills>>(
    (acc, skill) => {
      const key = skill.category ?? "Autres";
      if (!acc[key]) {
        acc[key] = [];
      }
      acc[key].push(skill);
      return acc;
    },
    {},
  );

  return (
    <main>
      <h1>Compétences</h1>
      {Object.entries(groupedSkills).map(([category, categorySkills]) => (
        <section key={category}>
          <h2>{category}</h2>
          <ul>
            {categorySkills.map((skill) => (
              <li key={skill.id}>{skill.name}</li>
            ))}
          </ul>
        </section>
      ))}
    </main>
  );
}
