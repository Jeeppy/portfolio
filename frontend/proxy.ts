import { NextResponse } from "next/server";
import { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  if (request.nextUrl.pathname === "/admin/login") {
    return NextResponse.next();
  }

  const token = request.cookies.get("token");
  if (!token) {
    return NextResponse.redirect(new URL("/admin/login", request.url));
  } else {
    return NextResponse.next();
  }
}

export const config = {
  matcher: ["/admin/:path*"],
};
