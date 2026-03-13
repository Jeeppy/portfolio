import { apiFetch } from "@/lib/api";
import { Profile } from "@/types/api";
import { Link } from "@/i18n/navigation";
import { getTranslations } from "next-intl/server";
import { FolderOpen, Mail } from "lucide-react";
import PlatformIcon from "@/components/icons/PlatformIcon";

export const dynamic = "force-dynamic";

export default async function Home() {
  const t = await getTranslations("home");
  const profile = await apiFetch<Profile>("/api/profile");
  const socialLinks = profile.social_links.map((link) => (
    <li key={link.id}>
      <Link
        href={link.url}
        className="flex h-9 w-9 items-center justify-center rounded-full border border-gray-200 text-gray-500 transition-colors hover:border-blue-600 hover:text-blue-600"
        title={link.platform}
        target="_blank"
      >
        <PlatformIcon platform={link.platform} size={16} className="text-xs" />
      </Link>
    </li>
  ));

  return (
    <main className="min-h-[calc(100vh-4rem)]">
      <div className="mx-auto flex max-w-5xl flex-col items-center gap-12 px-6 py-20 lg:flex-row">
        <div className="flex flex-1 flex-col gap-5">
          <h1 className="bg-linear-to-r from-indigo-600 to-blue-500 bg-clip-text text-center text-4xl leading-tight font-bold text-transparent">
            {profile.title}
          </h1>
          <p className="text-justify leading-relaxed text-gray-600">
            {profile.bio}
          </p>
          <div className="mt-2 flex gap-4">
            <Link
              href="/projects"
              className="flex items-center gap-2 rounded-lg border border-gray-300 px-6 py-3 text-sm font-medium text-gray-700 transition-colors hover:border-blue-600 hover:text-blue-600"
            >
              <FolderOpen size={16} />
              {t("see-my-projects")}
            </Link>
            <Link
              href="/contact"
              className="flex items-center gap-2 rounded-lg bg-blue-600 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-blue-700"
            >
              <Mail size={16} />
              {t("contact-me")}
            </Link>
          </div>
          <ul className="mt-4 flex gap-4">{socialLinks}</ul>
        </div>

        <div className="w-full flex-1">
          <div className="overflow-hidden rounded-xl bg-gray-900 shadow-2xl">
            <div className="flex items-center gap-2 bg-gray-800 px-4 py-3">
              <span className="h-3 w-3 rounded-full bg-red-500" />
              <span className="h-3 w-3 rounded-full bg-yellow-500" />
              <span className="h-3 w-3 rounded-full bg-green-500" />
              <span className="ml-3 text-xs text-gray-400">developer.py</span>
            </div>
            <div className="p-6 font-mono text-sm leading-7">
              <p>
                <span className="text-blue-300">developer: </span>
                <span className="text-purple-300">dict[str, str]</span>
                <span className="text-white"> =</span>
                <span className="text-white">{" {"}</span>
              </p>
              <p className="pl-6">
                <span className="text-green-300">
                  {'"'}full_name{'"'}
                </span>
                <span className="text-white">: </span>
                <span className="text-yellow-300">
                  {'"'}
                  {profile.full_name}
                  {'"'}
                </span>
                <span className="text-white">,</span>
              </p>
              <p className="pl-6">
                <span className="text-green-300">
                  {'"'}title{'"'}
                </span>
                <span className="text-white">: </span>
                <span className="text-yellow-300">
                  {'"'}
                  {profile.title}
                  {'"'}
                </span>
                <span className="text-white">,</span>
              </p>
              <p className="pl-6">
                <span className="text-green-300">
                  {'"'}location{'"'}
                </span>
                <span className="text-white">: </span>
                <span className="text-yellow-300">
                  {'"'}
                  {profile.location}
                  {'"'}
                </span>
                <span className="text-white">,</span>
              </p>
              <p className="pl-6">
                <span className="text-green-300">
                  {'"'}available{'"'}
                </span>
                <span className="text-white">: </span>
                <span className="text-orange-300">True</span>
                <span className="text-white">,</span>
              </p>
              <p className="text-white">{"}"}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
