import { NextIntlClientProvider } from "next-intl";
import { getMessages, getTranslations } from "next-intl/server";
import { Link } from "@/i18n/navigation";
import LocaleSwitcher from "@/components/LocaleSwitcher";
import Providers from "../providers";
import { Geist, Geist_Mono } from "next/font/google";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

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
    <html lang={locale}>
      <body
        className={`${geistSans.variable} ${geistMono.variable} min-h-screen bg-linear-to-b from-blue-50 to-white antialiased`}
      >
        <NextIntlClientProvider locale={locale} messages={messages}>
          <nav className="fixed top-0 right-0 left-0 z-50 bg-white/95 shadow-md backdrop-blur-sm">
            <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-10">
              <Link
                href="/"
                className="flex items-center gap-1 text-base font-semibold text-gray-900"
              >
                <span className="text-blue-600">&lt;</span>
                {t("logo")}
                <span className="text-blue-600">/&gt;</span>
              </Link>
              <div className="flex items-center gap-6">
                <Link
                  href="/"
                  className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
                >
                  {t("home")}
                </Link>
                <Link
                  href="/projects"
                  className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
                >
                  {t("projects")}
                </Link>
                <Link
                  href="/skills"
                  className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
                >
                  {t("skills")}
                </Link>
                <Link
                  href="/experiences"
                  className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
                >
                  {t("experiences")}
                </Link>
                <Link
                  href="/contact"
                  className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
                >
                  {t("contact")}
                </Link>
                <LocaleSwitcher />
              </div>
            </div>
          </nav>
          <div className="h-16" />

          <Providers>{children}</Providers>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
