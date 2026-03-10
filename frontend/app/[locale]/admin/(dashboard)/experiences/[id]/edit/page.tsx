import ExperienceForm from "@/components/admin/experiences/ExperienceForm";
import { ApiError, apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Experience } from "@/types/api";
import { notFound } from "next/navigation";

export default async function EditExperiencePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const token = getToken();
  let experience: Experience | undefined = undefined;
  try {
    experience = await apiFetch<Experience>(`/api/experiences/${id}`);
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
      <ExperienceForm initialData={experience} token={await token} />
    </div>
  );
}
