import SkillForm from "@/components/admin/skills/SkillForm";
import { adminFetch } from "@/lib/admin";
import { ApiError, apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Skill } from "@/types/api";
import { notFound } from "next/navigation";

export default async function EditSkillPage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const [token, { locale, id }] = await Promise.all([getToken(), params]);
  let skill: Skill | undefined = undefined;
  try {
    skill = await adminFetch(
      () => apiFetch<Skill>(`/api/skills/${id}`),
      locale,
    );
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
      <SkillForm initialData={skill} token={token} />
    </div>
  );
}
