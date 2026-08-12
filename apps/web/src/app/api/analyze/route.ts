import { NextResponse } from "next/server";
import { analysisRequestSchema } from "@/schemas/readmatch";
import { getBook } from "@/domain/repositories/catalog";
import { retrieveEvidence } from "@/domain/retrieval/evidence-retriever";
import { getModelProvider } from "@/domain/models/model-provider";
import { validateAnalysisResult } from "@/domain/analysis/validate-result";

export async function POST(request: Request) {
  try {
    const input = analysisRequestSchema.parse(await request.json());
    const book = getBook(input.bookId);

    if (!book || book.catalogStatus !== "active") {
      return NextResponse.json({ error: "该作品暂未收录" }, { status: 404 });
    }

    const evidence = retrieveEvidence(input.bookId, [
      ...input.positivePreferenceIds,
      ...input.hardConstraintIds,
    ]);
    const provider = getModelProvider();
    const result = validateAnalysisResult(await provider.analyze(input, evidence));

    return NextResponse.json({ result, book });
  } catch (error) {
    const message = error instanceof Error ? error.message : "分析失败";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}

