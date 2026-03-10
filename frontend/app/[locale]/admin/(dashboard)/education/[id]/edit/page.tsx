import EducationForm from "@/components/admin/education/EducationForm";
import { ApiError, apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Education } from "@/types/api";
import { notFound } from "next/navigation";

export default async function EditEducationPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const token = getToken();
  let education: Education | undefined = undefined;
  try {
    education = await apiFetch<Education>(`/api/education/${id}`);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return notFound();
    }
    throw error;
  }
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">
        Modifier - {education.school}
      </h1>
      <EducationForm initialData={education} token={await token} />
    </div>
  );
}
