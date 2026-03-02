"use client";

import { useRouter } from "next/navigation";

export default function LogoutButton() {
  const router = useRouter();

  async function handleLogout() {
    await fetch("/api/auth/logout", { method: "DELETE" });
    router.push("/admin/login");
  }

  return <button onClick={handleLogout}>Déconnexion</button>;
}
