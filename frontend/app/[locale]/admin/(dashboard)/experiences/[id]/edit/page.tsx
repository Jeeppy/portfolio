import ExperienceForm from "@/components/admin/experiences/ExperienceForm";
import { adminFetch } from "@/lib/admin";
import { ApiError, apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Experience } from "@/types/api";
import { notFound } from "next/navigation";

export default async function EditExperiencePage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const [token, { locale, id }] = await Promise.all([getToken(), params]);
  let experience: Experience | undefined = undefined;
  try {
    experience = await adminFetch(
      () => apiFetch<Experience>(`/api/experiences/${id}`),
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
        Modifier - {experience.company}
      </h1>
      <ExperienceForm initialData={experience} token={token} />
    </div>
  );
}
