import ExperienceForm from "@/components/admin/experiences/ExperienceForm";
import { getToken } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function NewExperiencePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const [token, locale] = await Promise.all([getToken(), params]);
  if (!token) redirect(`/${locale}/admin/login`);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">
        Nouvelle expérience
      </h1>
      <ExperienceForm token={token} />
    </div>
  );
}
