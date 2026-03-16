import EducationForm from "@/components/admin/education/EducationForm";
import { adminFetch } from "@/lib/admin";
import { ApiError, apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Education } from "@/types/api";
import { notFound, redirect } from "next/navigation";

export default async function EditEducationPage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const { locale, id } = await params;
  const token = await getToken();
  if (!token) redirect(`/${locale}/admin/login`);

  let education: Education | undefined = undefined;
  try {
    education = await adminFetch(
      () => apiFetch<Education>(`/api/education/${id}`),
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
        Modifier - {education.school}
      </h1>
      <EducationForm initialData={education} token={token} />
    </div>
  );
}
