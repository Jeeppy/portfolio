"use client";

import { useRouter, usePathname } from "@/i18n/navigation";
import { useLocale } from "next-intl";

export default function LocaleSwitcher() {
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();

  function switchLocale(newLocale: string) {
    router.replace(pathname, { locale: newLocale });
  }

  return (
    <div>
      <button
        onClick={() => switchLocale(locale === "fr" ? "en" : "fr")}
        className="transition-color cursor-pointer px-3 py-1 text-xs font-semibold text-gray-600 hover:text-blue-600"
      >
        {locale === "fr" ? "🇬🇧" : "🇫🇷"}
      </button>
    </div>
  );
}
