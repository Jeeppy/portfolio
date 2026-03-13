"use client";

import { useRouter, usePathname } from "@/i18n/navigation";
import { useLocale } from "next-intl";
import { FR, GB } from "country-flag-icons/react/3x2";

export default function LocaleSwitcher({
  mobile = false,
}: {
  mobile?: boolean;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();
  const flagStyle = "h-auto w-5";
  const FlagComponent = locale === "fr" ? GB : FR;
  const label = locale === "fr" ? "English" : "Français";

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
      {mobile ? (
        <span className="flex items-center gap-2">
          {label} <FlagComponent className={flagStyle} />
        </span>
      ) : (
        <FlagComponent className={flagStyle} />
      )}
    </button>
  );
}
