import ContactTable from "@/components/admin/contact/ContactTable";
import { adminFetch } from "@/lib/admin";
import { apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { ContactMessage } from "@/types/api";

export default async function ContactPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const [token, { locale }] = await Promise.all([getToken(), params]);
  const messages = await adminFetch(
    () =>
      apiFetch<ContactMessage[]>("/api/admin/contact", {
        headers: { Authorization: `Bearer ${token}` },
      }),
    locale,
  );

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Messages</h1>
      <ContactTable messages={messages} token={token} />
    </div>
  );
}
