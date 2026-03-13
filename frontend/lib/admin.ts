import { redirect } from "next/navigation";
import { ApiError } from "./api";

export async function adminFetch<T>(
  fn: () => Promise<T>,
  locale: string,
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      return redirect(`/${locale}/admin/login`);
    } else {
      throw error;
    }
  }
}
