import ContactForm from "./ContactForm";
import { getTranslations } from "next-intl/server";

export const dynamic = "force-dynamic";

export default async function ContactPage() {
  const t = await getTranslations("contact");
  return (
    <main>
      <h1>{t("title")}</h1>
      <ContactForm />
    </main>
  );
}
