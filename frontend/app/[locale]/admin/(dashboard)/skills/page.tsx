import SkillsTable from "@/components/admin/skills/SkillsTable";
import { apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Skill } from "@/types/api";
import { Link } from "@/i18n/navigation";
import { Plus } from "lucide-react";

export default async function AdminSkillsPage() {
  const skills = await apiFetch<Skill[]>("/api/skills");
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Compétences</h1>
      <SkillsTable skills={skills} token={await getToken()} />
      <div className="mt-4 flex justify-end">
        <Link
          href="/admin/skills/new"
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500"
        >
          <Plus size={16} />
          Nouvelle compétence
        </Link>
      </div>
    </div>
  );
}
