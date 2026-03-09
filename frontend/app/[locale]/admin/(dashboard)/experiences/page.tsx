import ExperiencesTable from "@/components/admin/experiences/ExperienceTable";
import { apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Experience } from "@/types/api";
import { Link } from "@/i18n/navigation";
import { Plus } from "lucide-react";

export default async function ExperiencesPage() {
  const experiences = await apiFetch<Experience[]>("/api/experiences");
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Expériences</h1>
      <ExperiencesTable experiences={experiences} token={await getToken()} />
      <div className="mt-4 flex justify-end">
        <Link
          href="/admin/experiences/new"
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500"
        >
          <Plus size={16} />
          Nouvelle expérience
        </Link>
      </div>
    </div>
  );
}
