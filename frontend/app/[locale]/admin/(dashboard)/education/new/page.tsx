import EducationForm from "@/components/admin/education/EducationForm";
import { getToken } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function NewEducationPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const [token, { locale }] = await Promise.all([getToken(), params]);
  if (!token) redirect(`/${locale}/admin/login`);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">
        Nouvelle formation
      </h1>
      <EducationForm token={await getToken()} />
    </div>
  );
}
