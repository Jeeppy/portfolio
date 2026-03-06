import { apiFetch } from "@/lib/api";
import { Skill } from "@/types/api";
import { getTranslations } from "next-intl/server";

export const dynamic = "force-dynamic";

export default async function SkillsPage() {
  const t = await getTranslations("skills");
  const skills = await apiFetch<Skill[]>("/api/skills");
  const groupedSkills = skills.reduce<Record<string, typeof skills>>(
    (acc, skill) => {
      const key = skill.category ?? t("other");
      if (!acc[key]) {
        acc[key] = [];
      }
      acc[key].push(skill);
      return acc;
    },
    {},
  );

  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <h1 className="mb-10 text-center text-3xl font-bold text-gray-900">
        {t("title")}
      </h1>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {Object.entries(groupedSkills).map(([category, categorySkills]) => (
          <div
            key={category}
            className="flex flex-col overflow-hidden rounded-xl bg-white shadow-md transition-all hover:shadow-md"
          >
            <div className="flex flex-1 flex-col p-5">
              <h2 className="mb-4 text-center text-base font-semibold text-gray-900 transition-colors">
                {category}
              </h2>
              <div className="flex flex-wrap justify-center gap-2">
                {categorySkills.map((skill) => (
                  <span
                    key={skill.id}
                    className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-600"
                  >
                    {skill.name}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
