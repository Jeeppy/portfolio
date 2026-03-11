"use client";

import { Profile } from "@/types/api";
import { useRouter } from "@/i18n/navigation";
import { SyntheticEvent, useRef, useState } from "react";
import { Link, Plus, Save, Trash2, Upload } from "lucide-react";
import { ApiError, apiFetch } from "@/lib/api";

export default function ProfileForm({
  initialData,
  token,
}: {
  initialData: Profile;
  token?: string;
}) {
  const router = useRouter();
  const [form, setForm] = useState({
    full_name: initialData?.full_name ?? "",
    title: initialData?.title ?? "",
    bio: initialData?.bio ?? "",
    email: initialData?.email ?? "",
    location: initialData?.location ?? "",
  });
  const [socialLinks, setSocialLinks] = useState<
    { platform: string; url: string }[]
  >(
    initialData?.social_links.map(({ platform, url }) => ({ platform, url })) ??
      [],
  );
  const [error, setError] = useState<string | null>(null);
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const avatarInputRef = useRef<HTMLInputElement>(null);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const resumeInputRef = useRef<HTMLInputElement>(null);

  function guessPlatform(url: string): string {
    try {
      return new URL(url).hostname.replace("www.", "");
    } catch {
      return "";
    }
  }

  async function handleSubmit(e: SyntheticEvent<HTMLElement>) {
    e.preventDefault();

    try {
      await apiFetch("/api/admin/profile", {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...form,
          title: form.title || null,
          bio: form.bio || null,
          email: form.email || null,
          location: form.location || null,
          social_links: socialLinks || null,
        }),
      });
      router.refresh();
    } catch (error) {
      if (error instanceof ApiError) {
        setError("Une erreur est survenue.");
      } else {
        throw error;
      }
    }
  }

  async function handleAvatarUpload() {
    if (!avatarFile) return;
    const fd = new FormData();
    fd.append("file", avatarFile);
    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/admin/profile/avatar`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: fd,
    });
    setAvatarFile(null);
    router.refresh();
  }

  async function handleAvatarDelete() {
    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/admin/profile/avatar`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    router.refresh();
  }

  async function handleResumeUpload() {
    if (!resumeFile) return;
    const fd = new FormData();
    fd.append("file", resumeFile);
    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/admin/profile/resume`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: fd,
    });
    setResumeFile(null);
    router.refresh();
  }

  async function handleResumeDelete() {
    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/admin/profile/resume`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    router.refresh();
  }

  return (
    <form onSubmit={handleSubmit} className="flex max-w-lg flex-col gap-5">
      {error && <p className="text-sm text-red-500">{error}</p>}
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Nom complet
        </label>
        <input
          name="full_name"
          value={form.full_name}
          onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Email
        </label>
        <input
          name="email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Poste
        </label>
        <input
          name="title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Localisation
        </label>
        <input
          name="location"
          value={form.location}
          onChange={(e) => setForm({ ...form, location: e.target.value })}
          className="block w-full rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="block text-sm/6 font-semibold text-gray-700">
          Bio
        </label>
        <textarea
          name="bio"
          value={form.bio}
          onChange={(e) => setForm({ ...form, bio: e.target.value })}
          className="block h-32 w-full resize-none rounded-md border border-gray-400 px-3.5 py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
        />
      </div>
      <div className="flex flex-col gap-1">
        <div className="flex items-center justify-between">
          <label className="text-sm/6 font-semibold text-gray-700">
            Liens sociaux
          </label>
          <button
            type="button"
            className="flex cursor-pointer items-center gap-1 rounded-md px-2.5 py-1 text-sm font-semibold text-indigo-600 hover:text-indigo-500"
            onClick={() =>
              setSocialLinks([...socialLinks, { platform: "", url: "" }])
            }
          >
            <Plus size={16} />
          </button>
        </div>
        <div>
          <ul className="mb-3 flex flex-col gap-2">
            {socialLinks?.map((socialLink, index) => (
              <li key={index} className="flex items-center gap-2">
                <div className="relative flex flex-1 items-center">
                  <Link size={14} className="absolute left-2.5 text-gray-400" />
                  <input
                    placeholder="Liens"
                    value={socialLink.url}
                    onChange={(e) => {
                      const updated = [...socialLinks];
                      updated[index] = {
                        url: e.target.value,
                        platform: guessPlatform(e.target.value),
                      };
                      setSocialLinks(updated);
                    }}
                    className="block w-full flex-1 rounded-md border border-gray-400 px-3 py-1.5 pl-8 text-sm text-gray-900 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-500/50"
                  />
                  <button
                    onClick={() =>
                      setSocialLinks(socialLinks.filter((_, i) => i !== index))
                    }
                    type="button"
                    className="cursor-pointer px-2 text-red-500 hover:text-red-700"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="flex flex-col gap-1">
        <label className="text-sm/6 font-semibold text-gray-700">Avatar</label>
        <div className="flex items-center gap-2">
          <input
            ref={avatarInputRef}
            type="file"
            accept="image/*"
            onChange={(e) => setAvatarFile(e.target.files?.[0] ?? null)}
            className="hidden"
          />
          <button
            className="flex-1 cursor-pointer rounded-md border border-gray-400 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50"
            type="button"
            onClick={() => avatarInputRef.current?.click()}
          >
            {avatarFile ? avatarFile.name : "Choisir un fichier"}
          </button>
          <button
            type="button"
            onClick={handleAvatarUpload}
            disabled={!avatarFile}
            className="flex cursor-pointer items-center gap-2 rounded-md bg-indigo-600 px-4 py-1.5 text-sm font-semibold text-white hover:bg-indigo-500 disabled:opacity-40"
          >
            <Upload size={14} />
            Envoyer
          </button>
        </div>
        {initialData.avatar_filename && !avatarFile && (
          <div className="text-xs text-gray-400">
            Actuel: {initialData.avatar_filename}
            <button
              type="button"
              className="cursor-pointer px-2 text-red-500 hover:text-red-700"
              onClick={() => handleAvatarDelete()}
            >
              <Trash2 size={14} />
            </button>
          </div>
        )}
      </div>
      <div className="flex flex-col gap-1">
        <label className="text-sm/6 font-semibold text-gray-700">CV</label>
        <div className="flex items-center gap-2">
          <input
            ref={resumeInputRef}
            type="file"
            accept="application/pdf"
            onChange={(e) => setResumeFile(e.target.files?.[0] ?? null)}
            className="hidden"
          />
          <button
            className="flex-1 cursor-pointer rounded-md border border-gray-400 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50"
            type="button"
            onClick={() => resumeInputRef.current?.click()}
          >
            {resumeFile ? resumeFile.name : "Choisir un fichier"}
          </button>
          <button
            type="button"
            onClick={handleResumeUpload}
            disabled={!resumeFile}
            className="flex cursor-pointer items-center gap-2 rounded-md bg-indigo-600 px-4 py-1.5 text-sm font-semibold text-white hover:bg-indigo-500 disabled:opacity-40"
          >
            <Upload size={14} />
            Envoyer
          </button>
        </div>
        {initialData.resume_filename && !resumeFile && (
          <div className="text-xs text-gray-400">
            Actuel: {initialData.resume_filename}
            <button
              type="button"
              className="cursor-pointer px-2 text-red-500 hover:text-red-700"
              onClick={() => handleResumeDelete()}
            >
              <Trash2 size={14} />
            </button>
          </div>
        )}
      </div>
      <div className="flex justify-end">
        <button
          type="submit"
          className="flex cursor-pointer items-center gap-2 rounded-md bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-indigo-500"
        >
          <Save size={16} />
          Enregistrer
        </button>
      </div>
    </form>
  );
}
