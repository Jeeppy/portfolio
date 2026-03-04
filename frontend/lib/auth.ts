import { cookies } from "next/headers";

export async function getToken() {
  const cookieStore = await cookies();
  return cookieStore.get("token")?.value;
}

export function getClientToken() {
  return document.cookie
    .split("; ")
    .find((c) => c.startsWith("token="))
    ?.split("=")[1];
}
