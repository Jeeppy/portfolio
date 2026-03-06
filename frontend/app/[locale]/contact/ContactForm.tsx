"use client";

import { apiFetch } from "@/lib/api";
import { ContactMessage } from "@/types/api";
import { Send } from "lucide-react";
import { useTranslations } from "next-intl";

export default function ContactForm() {
  const t = useTranslations("contact");

  return (
    <div className="rounded-xl bg-white p-8 shadow-md">
      <form action={handleSubmit} className="mx-auto max-w-xl">
        <div className="mb-3 flex flex-col gap-1">
          <label
            htmlFor="name"
            className="block text-sm/6 font-semibold text-gray-700"
          >
            {t("name")}
          </label>
          <input
            id="name"
            name="name"
            className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
          ></input>
        </div>
        <div className="mb-3 flex flex-col gap-1">
          <label
            htmlFor="email"
            className="block text-sm/6 font-semibold text-gray-700"
          >
            {t("email")}
          </label>
          <input
            name="email"
            className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
          ></input>
        </div>
        <div className="mb-3 flex flex-col gap-1">
          <label
            htmlFor="subject"
            className="block text-sm/6 font-semibold text-gray-700"
          >
            {t("subject")}
          </label>
          <input
            name="subject"
            className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
          ></input>
        </div>
        <div className="mb-3 flex flex-col gap-1">
          <label
            htmlFor="message"
            className="block text-sm/6 font-semibold text-gray-700"
          >
            {t("message")}
          </label>
          <textarea
            name="message"
            rows={5}
            placeholder={t("messagePlaceholder")}
            className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
          ></textarea>
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            className="flex items-center gap-2 rounded-md bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-blue-700"
          >
            <Send size={16} />
            {t("submit")}
          </button>
        </div>
      </form>
    </div>
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
