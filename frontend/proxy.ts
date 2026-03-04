import { NextResponse } from "next/server";
import { NextRequest } from "next/server";
import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

const intlMiddleware = createMiddleware(routing);

export function proxy(request: NextRequest) {
  const pathname = request.nextUrl.pathname;
  const isAdminRoute = routing.locales.some((locale) =>
    pathname.startsWith(`/${locale}/admin`),
  );

  if (isAdminRoute) {
    if (pathname.endsWith("/admin/login")) {
      return NextResponse.next();
    }

    const token = request.cookies.get("token");
    if (!token) {
      const locale = pathname.split("/")[1];
      return NextResponse.redirect(
        new URL(`/${locale}/admin/login`, request.url),
      );
    } else {
      return NextResponse.next();
    }
  }
  return intlMiddleware(request);
}

export const config = {
  matcher: ["/((?!api|_next|.*\\..*).*)"],
};
