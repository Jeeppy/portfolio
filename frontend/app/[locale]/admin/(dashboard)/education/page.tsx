import { apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Education } from "@/types/api";
import { Link } from "@/i18n/navigation";
import { Plus } from "lucide-react";
import EducationTable from "@/components/admin/education/EducationTable";
import { adminFetch } from "@/lib/admin";

export default async function EducationPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const [educations, token] = await Promise.all([
    adminFetch(() => apiFetch<Education[]>("/api/education"), locale),
    getToken(),
  ]);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Formations</h1>
      <EducationTable educations={educations} token={token} />
      <div className="mt-4 flex justify-end">
        <Link
          href="/admin/education/new"
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500"
        >
          <Plus size={16} />
          Nouvelle formation
        </Link>
      </div>
    </div>
  );
}
