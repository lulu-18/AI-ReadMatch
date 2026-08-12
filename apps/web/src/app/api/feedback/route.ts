import { NextResponse } from "next/server";
import { feedbackRequestSchema } from "@/schemas/readmatch";

export async function POST(request: Request) {
  try {
    const feedback = feedbackRequestSchema.parse(await request.json());
    console.info("[ReadMatch feedback]", feedback);
    return NextResponse.json({ ok: true, message: "反馈已记录（M1 Mock 模式）" });
  } catch {
    return NextResponse.json({ error: "反馈格式不正确" }, { status: 400 });
  }
}
