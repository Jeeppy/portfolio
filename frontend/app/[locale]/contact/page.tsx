import ContactForm from "./ContactForm";
import { getTranslations } from "next-intl/server";

export const dynamic = "force-dynamic";

export default async function ContactPage() {
  const t = await getTranslations("contact");
  return (
    <main className="mx-auto max-w-2xl px-6 py-16">
      <h1 className="mb-10 text-center text-3xl font-bold text-gray-900">
        {t("title")}
      </h1>
      <ContactForm />
    </main>
  );
}
