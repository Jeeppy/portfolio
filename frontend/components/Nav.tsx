"use client";

import { Link } from "@/i18n/navigation";
import { useTranslations } from "next-intl";
import { useState } from "react";
import LocaleSwitcher from "./LocaleSwitcher";
import { Menu, X } from "lucide-react";

export default function Nav() {
  const t = useTranslations("nav");
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 right-0 left-0 z-50 bg-white/95 shadow-md backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6 md:px-10">
        <Link
          href="/"
          className="flex items-center gap-1 text-base font-semibold text-gray-900"
        >
          <span className="text-blue-600">&lt;</span>
          {t("logo")}
          <span className="text-blue-600">/&gt;</span>
        </Link>
        <div className="hidden items-center gap-6 md:flex">
          <Link
            href="/"
            className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
          >
            {t("home")}
          </Link>
          <Link
            href="/projects"
            className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
          >
            {t("projects")}
          </Link>
          <Link
            href="/skills"
            className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
          >
            {t("skills")}
          </Link>
          <Link
            href="/experiences"
            className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
          >
            {t("experiences")}
          </Link>
          <Link
            href="/contact"
            className="text-sm font-bold text-gray-900 transition-colors hover:text-blue-600"
          >
            {t("contact")}
          </Link>
          <LocaleSwitcher />
        </div>
        <button
          className="flex cursor-pointer text-gray-700 md:hidden"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X size={24} /> : <Menu size={25} />}
        </button>
      </div>
      {isOpen && (
        <div className="flex flex-col gap-4 border-t border-gray-100 bg-white px-6 py-4 md:hidden">
          <Link
            href="/"
            onClick={() => setIsOpen(false)}
            className="text-sm font-bold text-gray-900 hover:text-blue-600"
          >
            {t("home")}
          </Link>
          <Link
            href="/projects"
            onClick={() => setIsOpen(false)}
            className="text-sm font-bold text-gray-900 hover:text-blue-600"
          >
            {t("projects")}
          </Link>
          <Link
            href="/skills"
            onClick={() => setIsOpen(false)}
            className="text-sm font-bold text-gray-900 hover:text-blue-600"
          >
            {t("skills")}
          </Link>
          <Link
            href="/experiences"
            onClick={() => setIsOpen(false)}
            className="text-sm font-bold text-gray-900 hover:text-blue-600"
          >
            {t("experiences")}
          </Link>
          <Link
            href="/contact"
            onClick={() => setIsOpen(false)}
            className="text-sm font-bold text-gray-900 hover:text-blue-600"
          >
            {t("contact")}
          </Link>
          <LocaleSwitcher mobile />
        </div>
      )}
    </nav>
  );
}
