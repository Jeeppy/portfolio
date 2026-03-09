"use client";

import { useRouter } from "@/i18n/navigation";
import { LogOut } from "lucide-react";

export default function LogoutButton() {
  const router = useRouter();

  async function handleLogout() {
    await fetch("/api/auth/logout", { method: "DELETE" });
    router.push("/admin/login");
  }

  return (
    <button
      onClick={handleLogout}
      className="flex w-full cursor-pointer gap-2 rounded-lg px-3 py-2 text-left text-sm transition-colors hover:bg-slate-700 hover:text-white"
    >
      <LogOut size={16} />
      Déconnexion
    </button>
  );
}
