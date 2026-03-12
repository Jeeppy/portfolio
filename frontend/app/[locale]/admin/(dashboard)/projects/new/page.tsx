import ProjectForm from "@/components/admin/projects/ProjectForm";
import { getToken } from "@/lib/auth";

export default async function NewProjectPage() {
  const token = await getToken();
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Nouveau projet</h1>
      <ProjectForm token={token} />
    </div>
  );
}
