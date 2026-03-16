import { apiFetch } from "@/lib/api";
import { Education } from "@/types/api";
import { getTranslations } from "next-intl/server";

export default async function EducationPage() {
  const [educations, t] = await Promise.all([
    apiFetch<Education[]>("/api/education"),
    getTranslations("education"),
  ]);
  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="mb-10 text-center text-3xl font-bold text-gray-900">
        {t("title")}
      </h1>
      <div className="flex flex-col gap-6">
        {educations.map((education) => (
          <div
            key={education.id}
            className="rounded-xl bg-white p-6 shadow-md hover:shadow-xl"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-base font-semibold text-gray-900">
                  {education.degree}
                </h2>
                <div className="flex items-center gap-2">
                  <p className="text-sm font-medium text-blue-600">
                    {education.school}
                  </p>
                  {education.location && (
                    <p className="text-xs text-gray-400">
                      {education.location}
                    </p>
                  )}
                  {education.is_alternance && (
                    <span className="inline-block rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-600">
                      {t("alternance")}
                    </span>
                  )}
                </div>
              </div>
              <p className="text-xs whitespace-nowrap text-gray-500">
                {education.year}
              </p>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
