import SkillForm from "@/components/admin/skills/SkillForm";
import { getToken } from "@/lib/auth";

export default async function NewSkillPage() {
  const token = await getToken();
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">
        Nouvelle compétence
      </h1>
      <SkillForm token={token} />
    </div>
  );
}
