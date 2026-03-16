import ProfileForm from "@/components/admin/profile/ProfileForm";
import { adminFetch } from "@/lib/admin";
import { apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Profile } from "@/types/api";
import { redirect } from "next/navigation";

export default async function ProfilePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const [profile, token] = await Promise.all([
    adminFetch(() => apiFetch<Profile>("/api/profile"), locale),
    getToken(),
  ]);
  if (!token) redirect(`/${locale}/admin/login`);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Profile</h1>
      <ProfileForm initialData={profile} token={token} />
    </div>
  );
}
