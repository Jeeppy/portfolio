import SkillForm from "@/components/admin/skills/SkillForm";
import { getToken } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function NewSkillPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const [token, { locale }] = await Promise.all([getToken(), params]);
  if (!token) redirect(`/${locale}/admin/login`);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">
        Nouvelle compétence
      </h1>
      <SkillForm token={token} />
    </div>
  );
}
