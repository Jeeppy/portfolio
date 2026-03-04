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
      <button onClick={() => switchLocale("fr")} disabled={locale === "fr"}>
        FR
      </button>
      <button onClick={() => switchLocale("en")} disabled={locale === "en"}>
        EN
      </button>
    </div>
  );
}
