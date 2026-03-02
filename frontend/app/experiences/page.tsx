import { apiFetch } from "@/lib/api";
import { Profile } from "@/types/api";

export const dynamic = "force-dynamic";

export default async function ExperiencesPage() {
  const profile = await apiFetch<Profile>("/api/profile");
  const experiences = profile.experiences;

  return (
    <main>
      <h1>Experiences</h1>
      {experiences.map((experience) => (
        <section key={experience.id}>
          <h2>
            {experience.company} - {experience.position}
          </h2>
          <p>{experience.location}</p>
          <p>
            {new Date(experience.start_date).toLocaleDateString("fr-Fr", {
              year: "numeric",
              month: "long",
            })}
            {" à "}
            {experience.end_date
              ? new Date(experience.end_date).toLocaleDateString("fr-Fr", {
                  year: "numeric",
                  month: "long",
                })
              : "aujourd'hui"}
          </p>
          <p style={{ whiteSpace: "pre-line" }}>{experience.description}</p>
        </section>
      ))}
    </main>
  );
}
