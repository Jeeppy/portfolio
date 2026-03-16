import { apiFetch } from "@/lib/api";
import { Experience, Profile } from "@/types/api";
import { Link } from "@/i18n/navigation";
import { getTranslations } from "next-intl/server";
import { FolderOpen, Mail } from "lucide-react";
import PlatformIcon from "@/components/icons/PlatformIcon";
import TerminalMockup from "@/components/TerminalMockup";

export const dynamic = "force-dynamic";

export default async function Home() {
  const t = await getTranslations("home");
  const [profile, experiences] = await Promise.all([
    apiFetch<Profile>("/api/profile"),
    apiFetch<Experience[]>("/api/experiences"),
  ]);

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
        <TerminalMockup profile={profile} experiences={experiences} />
      </div>
    </main>
  );
}
