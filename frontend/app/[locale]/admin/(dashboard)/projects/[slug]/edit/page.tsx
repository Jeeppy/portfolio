import ProjectForm from "@/components/admin/projects/ProjectForm";
import { apiFetch, ApiError } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Project } from "@/types/api";
import { notFound } from "next/navigation";

export default async function EditProjectPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  let project: Project | undefined = undefined;
  try {
    project = await apiFetch<Project>(
      `/api/admin/projects/${(await params).slug}`,
      {
        headers: { Authorization: `Bearer ${await getToken()}` },
      },
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
      <ProjectForm initialData={project} />
    </div>
  );
}
