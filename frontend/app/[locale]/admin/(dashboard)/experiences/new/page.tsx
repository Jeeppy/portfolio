import ExperienceForm from "@/components/admin/experiences/ExperienceForm";
import { getToken } from "@/lib/auth";

export default async function NewExperiencePage() {
  const token = await getToken();
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">
        Nouvelle expérience
      </h1>
      <ExperienceForm token={token} />
    </div>
  );
}
