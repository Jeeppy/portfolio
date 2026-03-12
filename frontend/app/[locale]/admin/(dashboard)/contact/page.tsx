import ContactTable from "@/components/admin/contact/ContactTable";
import { ApiError, apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { ContactMessage } from "@/types/api";
import { redirect } from "next/navigation";

export default async function ContactPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const token = await getToken();
  let messages: ContactMessage[] = [];
  try {
    messages = await apiFetch<ContactMessage[]>("/api/admin/contact", {
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      const { locale } = await params;
      return redirect(`/${locale}/admin/login`);
    }
    throw error;
  }

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Messages</h1>
      <ContactTable messages={messages} token={token} />
    </div>
  );
}
