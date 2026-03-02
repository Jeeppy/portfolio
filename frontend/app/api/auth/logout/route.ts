import { NextRequest, NextResponse } from "next/server";

export async function DELETE(request: NextRequest) {
  const response = NextResponse.redirect(new URL("/admin/login", request.url));
  response.cookies.delete("token");

  return response;
}
