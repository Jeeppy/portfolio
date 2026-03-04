import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Jean-Patrick Debaëne - Développeur backend",
  description:
    "Développeur backend polyvalent avec 15 ans d'expérience dans la conception d'APIs et d'applications métier.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return children;
}
