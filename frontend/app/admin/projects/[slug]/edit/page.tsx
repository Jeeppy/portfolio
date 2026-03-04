import ProjectForm from "@/components/admin/projects/ProjectForm";
import { apiFetch, ApiError } from "@/lib/api";
import { Project } from "@/types/api";
import { cookies } from "next/headers";
import { notFound } from "next/navigation";

export default async function EditProjectPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value;
  let project: Project | undefined = undefined;
  try {
    project = await apiFetch<Project>(
      `/api/admin/projects/${(await params).slug}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return notFound();
    }
  }
  return <ProjectForm initialData={project} />;
}
