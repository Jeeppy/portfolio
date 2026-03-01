"use client";

import { apiFetch } from "@/lib/api";
import { ContactMessage } from "@/types/api";

export default function ContactForm() {
  return (
    <form action={handleSubmit}>
      <input name="name"></input>
      <input name="email"></input>
      <input name="subject"></input>
      <textarea name="message"></textarea>
      <button type="submit">Envoyer</button>
    </form>
  );
}

async function handleSubmit(formData: FormData) {
  const name = formData.get("name") as string;
  const email = formData.get("email") as string;
  const subject = formData.get("subject") as string;
  const message = formData.get("message") as string;

  await apiFetch<ContactMessage>("/api/contact/", {
    method: "POST",
    body: JSON.stringify({ name, email, subject, message }),
  });
}
