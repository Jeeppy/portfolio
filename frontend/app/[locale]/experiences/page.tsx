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
    <main>
      <h1>{t("title")}</h1>
      {experiences.map((experience) => (
        <section key={experience.id}>
          <h2>
            {experience.company} - {experience.position}
          </h2>
          <p>{experience.location}</p>
          <p>
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
          <p style={{ whiteSpace: "pre-line" }}>{experience.description}</p>
        </section>
      ))}
    </main>
  );
}
