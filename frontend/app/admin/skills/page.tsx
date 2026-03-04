import SkillsTable from "@/components/admin/skills/SkillsTable";
import { apiFetch } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Skill } from "@/types/api";
import Link from "next/link";

export default async function AdminSkillsPage() {
  const skills = await apiFetch<Skill[]>("/api/skills");
  return (
    <div>
      <Link href="/admin/skills/new">
        <button>Nouvelle compétence</button>
      </Link>
      <SkillsTable skills={skills} token={await getToken()} />
    </div>
  );
}
