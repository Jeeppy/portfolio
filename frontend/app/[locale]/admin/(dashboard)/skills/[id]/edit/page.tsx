import SkillForm from "@/components/admin/skills/SkillForm";
import { ApiError, apiFetch } from "@/lib/api";
import { Skill } from "@/types/api";
import { notFound } from "next/navigation";

export default async function EditSkillPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  let skill: Skill | undefined = undefined;
  try {
    skill = await apiFetch<Skill>(`/api/skills/${(await params).id}`);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return notFound();
    }
    throw error;
  }
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">
        Modifier - {skill.name}
      </h1>
      <SkillForm initialData={skill} />
    </div>
  );
}
