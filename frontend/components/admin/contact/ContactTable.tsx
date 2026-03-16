"use client";

import { apiFetch } from "@/lib/api";
import { ContactMessage } from "@/types/api";
import { MailOpen, Trash2 } from "lucide-react";
import { Fragment, useState } from "react";

export default function ContactTable({
  messages,
  token,
}: {
  messages: ContactMessage[];
  token?: string;
}) {
  const [list, setList] = useState(messages);
  const [openId, setOpenId] = useState<number | null>(null);

  async function markAsRead(id: number) {
    const updated = await apiFetch<ContactMessage>(
      `/api/admin/contact/${id}/read`,
      {
        method: "PATCH",
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    setList((prev) => prev.map((m) => (m.id === id ? updated : m)));
  }

  async function deleteMessage(id: number) {
    await apiFetch(`/api/admin/contact/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    setList((prev) => prev.filter((m) => m.id !== id));
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="bg-slate-100 text-xs tracking-wider text-slate-500 uppercase">
            <th className="px-4 py-3 font-medium">Date</th>
            <th className="px-4 py-3 font-medium">Expediteur</th>
            <th className="px-4 py-3 font-medium">Sujet</th>
            <th className="px-4 py-3 font-medium">Lu</th>
            <th className="px-4 py-3 font-medium"></th>
          </tr>
        </thead>
        <tbody>
          {list.length === 0 ? (
            <tr>
              <td
                colSpan={5}
                className="px-4 py-8 text-center text-sm text-slate-400"
              >
                Aucun message
              </td>
            </tr>
          ) : (
            list.map((message) => (
              <Fragment key={message.id}>
                <tr
                  onClick={() =>
                    setOpenId(openId === message.id ? null : message.id)
                  }
                  className="cursor-pointer border-t border-slate-200 hover:bg-slate-100"
                >
                  <td className="px-4 py-3 text-slate-700">
                    {new Date(message.created_at).toLocaleDateString("fr-FR")}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {message.name} &lt;{message.email}&gt;
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {message.subject}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs font-medium ${message.read ? "bg-green-100 text-green-700" : "bg-orange-100 text-orange-700"}`}
                    >
                      {message.read ? "Lu" : "Non Lu"}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    <button
                      type="button"
                      disabled={message.read}
                      onClick={(e) => {
                        e.stopPropagation();
                        markAsRead(message.id);
                      }}
                      className="cursor-pointer rounded-md p-1.5 text-slate-400 transition-colors hover:bg-indigo-50 hover:text-indigo-600 disabled:cursor-default disabled:opacity-30"
                    >
                      <MailOpen size={16} />
                    </button>
                    <button
                      type="button"
                      className="cursor-pointer rounded-md p-1.5 text-slate-400 transition-colors hover:bg-red-50 hover:text-red-600"
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteMessage(message.id);
                      }}
                    >
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
                {openId === message.id && (
                  <tr className="bg-slate-50">
                    <td colSpan={5} className="px-4 py-3 text-slate-700">
                      {message.message}
                    </td>
                  </tr>
                )}
              </Fragment>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
