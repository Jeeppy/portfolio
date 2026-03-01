import { apiFetch } from "@/lib/api";
import { Profile } from "@/types/api";
import Link from "next/link";

export default async function Home() {
  const profile = await apiFetch<Profile>("/api/profile");
  const socialLinks = profile.social_links.map((link) => (
    <li key={link.id}>
      <Link href={link.url}>{link.platform}</Link>
    </li>
  ));
  return (
    <main>
      <h1>{profile.full_name}</h1>
      <p>{profile.title}</p>
      <p>{profile.bio}</p>
      <p>{profile.location}</p>
      <ul>{socialLinks}</ul>
    </main>
  );
}
