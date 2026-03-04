import Link from "next/link";

export default function AdminLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div>
      <nav>
        <ul>
          <li>
            <Link href="/admin/projects">Project</Link>
          </li>
        </ul>
      </nav>
      <main>{children}</main>
    </div>
  );
}
