"use client";

import { useRouter } from "@/i18n/navigation";

export default function LoginForm() {
  const router = useRouter();

  async function handleSubmit(formData: FormData) {
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    const response = await fetch(`/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (response.status === 200) {
      router.push("/admin");
    }
  }

  return (
    <form action={handleSubmit} className="flex flex-col gap-4">
      <div className="flex flex-col gap-1">
        <label className="text-sm font-bold text-slate-300">Email</label>
        <input
          name="email"
          type="email"
          className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-white placeholder-slate-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="text-sm font-bold text-slate-300">Mot de passe</label>
        <input
          name="password"
          type="password"
          className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-white placeholder-slate-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
        />
      </div>
      <button
        type="submit"
        className="mt-2 rounded-lg bg-indigo-600 py-2 font-medium text-white transition-colors hover:bg-indigo-500"
      >
        Connexion
      </button>
    </form>
  );
}
