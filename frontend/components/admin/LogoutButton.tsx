"use client";

import { useRouter } from "@/i18n/navigation";

export default function LogoutButton() {
  const router = useRouter();

  async function handleLogout() {
    await fetch("/api/auth/logout", { method: "DELETE" });
    router.push("/admin/login");
  }

  return <button onClick={handleLogout}>Déconnexion</button>;
}
