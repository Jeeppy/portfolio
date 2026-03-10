import EducationForm from "@/components/admin/education/EducationForm";
import { getToken } from "@/lib/auth";

export default async function NewEducationPage() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">
        Nouvelle formation
      </h1>
      <EducationForm token={await getToken()} />
    </div>
  );
}
