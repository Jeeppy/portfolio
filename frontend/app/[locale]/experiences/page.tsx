import { apiFetch } from "@/lib/api";
import { Profile } from "@/types/api";
import { getTranslations } from "next-intl/server";

export const dynamic = "force-dynamic";

export default async function ExperiencesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const profile = await apiFetch<Profile>("/api/profile");
  const experiences = profile.experiences;
  const t = await getTranslations("experiences");
  const locale = (await params).locale;
  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="mb-10 text-center text-3xl font-bold text-gray-900">
        {t("title")}
      </h1>
      <div className="flex flex-col gap-6">
        {experiences.map((experience) => (
          <div
            key={experience.id}
            className="rounded-xl bg-white p-6 shadow-md hover:shadow-xl"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-base font-semibold text-gray-900">
                  {experience.position}
                </h2>
                <p className="text-sm font-medium text-blue-600">
                  {experience.company}
                </p>
                {experience.location && (
                  <p className="mt-1 text-xs text-gray-500">
                    {experience.location}
                  </p>
                )}
              </div>
              <p className="text-xs whitespace-nowrap text-gray-500">
                {new Date(experience.start_date).toLocaleDateString(locale, {
                  year: "numeric",
                  month: "long",
                })}{" "}
                {t("to")}{" "}
                {experience.end_date
                  ? new Date(experience.end_date).toLocaleDateString(locale, {
                      year: "numeric",
                      month: "long",
                    })
                  : t("present")}
              </p>
            </div>
            {experience.description && (
              <p
                className="mt-3 text-sm leading-relaxed text-gray-600"
                style={{ whiteSpace: "pre-line" }}
              >
                {experience.description}
              </p>
            )}
          </div>
        ))}
      </div>
    </main>
  );
}
