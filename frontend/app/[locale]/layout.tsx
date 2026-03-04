import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import { Link } from "@/i18n/navigation";
import { getTranslations } from "next-intl/server";
import LocaleSwitcher from "@/components/LocaleSwitcher";

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const messages = await getMessages();
  const t = await getTranslations("nav");

  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      <nav>
        <Link href="/">{t("home")}</Link>
        <Link href="/projects">{t("projects")}</Link>
        <Link href="/skills">{t("skills")}</Link>
        <Link href="/experiences">{t("experiences")}</Link>
        <Link href="/contact">{t("contact")}</Link>
      </nav>
      <LocaleSwitcher />
      {children}
    </NextIntlClientProvider>
  );
}
