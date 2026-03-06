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
    <button
      onClick={() => switchLocale(locale === "fr" ? "en" : "fr")}
      className={
        mobile
          ? "self-start text-sm font-bold text-gray-900 hover:text-blue-600"
          : "cursor-pointer px-3 py-1 text-xs font-semibold text-gray-600 transition-colors hover:text-blue-600"
      }
    >
      {mobile ? t("switchLangMobile") : t("switchLang")}
    </button>
  );
}
