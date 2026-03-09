import LoginForm from "@/components/admin/LoginForm";

export default async function LoginPage() {
  return (
    <div className="w-full max-w-sm">
      <h1 className="mb-8 text-center text-2xl font-bold text-white">
        Administration
      </h1>
      <LoginForm />
    </div>
  );
}
