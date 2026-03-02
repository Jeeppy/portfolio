import ContactForm from "./ContactForm";

export const dynamic = "force-dynamic";

export default async function ContactPage() {
  return (
    <main>
      <h1>Contact</h1>
      <ContactForm />
    </main>
  );
}
