import { ReactNode } from "react";

export default function AuthLayout({
  children,
}: Readonly<{ children: ReactNode }>) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900">
      {children}
    </div>
  );
}
