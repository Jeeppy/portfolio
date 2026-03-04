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
    <form action={handleSubmit}>
      <input name="email"></input>
      <input name="password" type="password"></input>
      <button type="submit">Connexion</button>
    </form>
  );
}
