import ProjectForm from "@/components/admin/projects/ProjectForm";
import { getToken } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function NewProjectPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const [token, { locale }] = await Promise.all([getToken(), params]);
  if (!token) redirect(`/${locale}/admin/login`);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Nouveau projet</h1>
      <ProjectForm token={token} />
    </div>
  );
}
