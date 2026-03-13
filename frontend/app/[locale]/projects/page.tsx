import { apiFetch } from "@/lib/api";
import { Project } from "@/types/api";
import { Link } from "@/i18n/navigation";
import { getTranslations } from "next-intl/server";
import { ExternalLink } from "lucide-react";
import { SiGithub } from "@icons-pack/react-simple-icons";

export const dynamic = "force-dynamic";

export default async function ProjectsPage() {
  const projects = await apiFetch<Project[]>("/api/projects");
  const t = await getTranslations("project");
  const colors = [
    "bg-blue-100 text-blue-600",
    "bg-green-100 text-green-600",
    "bg-purple-100 text-purple-600",
    "bg-yellow-100 text-yellow-600",
    "bg-pink-100 text-pink-600",
  ];
  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <h1 className="mb-10 text-center text-3xl font-bold text-gray-900">
        {t("title")}
      </h1>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((project) => (
          <div
            key={project.id}
            className="flex flex-col overflow-hidden rounded-xl bg-white shadow-md transition-all hover:shadow-xl"
          >
            <div className="flex flex-1 flex-col p-5">
              <h2 className="mb-2 text-base font-semibold text-gray-900 transition-colors">
                {project.title}
              </h2>
              {project.description && (
                <p className="mb-4 flex-1 text-sm leading-relaxed text-gray-500">
                  {project.description}
                </p>
              )}
              {project.tags && project.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {project.tags.map((tag, i) => {
                    return (
                      <span
                        key={tag.id}
                        className={`rounded-full px-3 py-1 text-xs font-medium ${colors[i % colors.length]}`}
                      >
                        {tag.name}
                      </span>
                    );
                  })}
                </div>
              )}
              {(project.repository_url || project.demo_url) && (
                <div className="mt-auto flex gap-2 border-gray-100 pt-3">
                  {project.repository_url && (
                    <Link
                      href={project.repository_url}
                      target="_blank"
                      className="flex h-8 w-8 items-center justify-center rounded-full border border-gray-200 text-gray-500 transition-colors hover:border-blue-600 hover:text-blue-600"
                    >
                      <SiGithub size={14} />
                    </Link>
                  )}
                  {project.demo_url && (
                    <Link
                      href={project.demo_url}
                      target="_blank"
                      className="flex h-8 w-8 items-center justify-center rounded-full border border-gray-200 text-gray-500 transition-colors hover:border-blue-600 hover:text-blue-600"
                    >
                      <ExternalLink size={14} />
                    </Link>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
