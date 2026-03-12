import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import Providers from "../providers";
import { Geist, Geist_Mono } from "next/font/google";
import Nav from "@/components/Nav";

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

  return (
    <html lang={locale}>
      <body
        className={`${geistSans.variable} ${geistMono.variable} min-h-screen bg-linear-to-b from-blue-50 to-white antialiased`}
      >
        <NextIntlClientProvider locale={locale} messages={messages}>
          <Nav />
          <div className="h-16" />
          <Providers>{children}</Providers>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
