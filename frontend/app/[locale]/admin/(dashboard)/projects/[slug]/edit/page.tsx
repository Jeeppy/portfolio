import ProjectForm from "@/components/admin/projects/ProjectForm";
import { adminFetch } from "@/lib/admin";
import { apiFetch, ApiError } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Project } from "@/types/api";
import { notFound, redirect } from "next/navigation";

export default async function EditProjectPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const [token, { locale, slug }] = await Promise.all([getToken(), params]);
  if (!token) redirect(`/${locale}/admin/login`);

  let project: Project | undefined = undefined;
  try {
    project = await adminFetch(
      () =>
        apiFetch<Project>(`/api/admin/projects/${slug}`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
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
        Modifier - {project.title}
      </h1>
      <ProjectForm initialData={project} token={token} />
    </div>
  );
}
