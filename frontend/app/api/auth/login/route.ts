import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const body = await request.json();
  const email = body["email"];
  const password = body["password"];

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    },
  );

  if (response.status != 200) {
    return NextResponse.json({ error: "..." }, { status: 401 });
  } else {
    const data = await response.json();
    const token = data.access_token;
    const nextResponse = NextResponse.json({ ok: true });
    nextResponse.cookies.set("token", token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
    });
    return nextResponse;
  }
}
