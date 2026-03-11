import ProfileForm from "@/components/admin/profile/ProfileForm";
import { apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Profile } from "@/types/api";

export default async function ProfilePage() {
  const [profile, token] = await Promise.all([
    apiFetch<Profile>("/api/profile"),
    getToken(),
  ]);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-slate-800">Profile</h1>
      <ProfileForm initialData={profile} token={token} />
    </div>
  );
}
