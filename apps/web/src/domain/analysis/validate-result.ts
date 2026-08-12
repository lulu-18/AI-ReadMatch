import { analysisResultSchema, type AnalysisResult } from "@/schemas/readmatch";

export function validateAnalysisResult(result: AnalysisResult): AnalysisResult {
  const parsed = analysisResultSchema.parse(result);
  const invalidReferences = [
    ...parsed.matchPoints.flatMap((point) => point.evidenceIds),
    ...parsed.riskPoints.flatMap((point) => point.evidenceIds),
    ...parsed.conflictingViews.flatMap((point) => point.evidenceIds),
    ...parsed.hardConstraintChecks.flatMap((check) => check.evidenceIds),
  ].filter((id) => !parsed.retrievedEvidenceIds.includes(id));

  if (invalidReferences.length > 0) {
    throw new Error("结果引用了未检索的证据");
  }

  if (
    parsed.verdict === "likely_match" &&
    parsed.hardConstraintChecks.some((check) => check.status === "present")
  ) {
    throw new Error("综合判断与已确认硬性雷点冲突");
  }

  return parsed;
}
