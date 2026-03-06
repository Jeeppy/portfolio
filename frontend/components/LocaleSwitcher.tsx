"use client";

import { useRouter, usePathname } from "@/i18n/navigation";
import { useLocale, useTranslations } from "next-intl";

export default function LocaleSwitcher({
  mobile = false,
}: {
  mobile?: boolean;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();
  const t = useTranslations("nav");

  function switchLocale(newLocale: string) {
    router.replace(pathname, { locale: newLocale });
  }

  return (
    <div className="self-start">
      <button
        onClick={() => switchLocale(locale === "fr" ? "en" : "fr")}
        className={
          mobile
            ? "text-sm font-bold text-gray-900 hover:text-blue-600"
            : "transition-color cursor-pointer px-3 py-1 text-xs font-semibold text-gray-600 hover:text-blue-600"
        }
      >
        {mobile ? t("switchLangMobile") : t("switchLang")}
      </button>
    </div>
  );
}
