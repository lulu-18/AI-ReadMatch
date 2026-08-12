import type {
  AnalysisRequest,
  AnalysisResult,
  Evidence,
  PreferenceOption,
} from "@/schemas/readmatch";
import { getBook, getOption } from "@/domain/repositories/catalog";

function sourceLabel(sourceType: Evidence["sourceType"]): string {
  return {
    official: "官方作品信息",
    publisher_summary: "出版/书籍简介",
    reader_review: "读者评论",
    reader_summary: "读者整理",
  }[sourceType];
}

function strengthFromEvidence(items: Evidence[]): Evidence["strength"] {
  if (items.some((item) => item.strength === "high")) return "high";
  if (items.some((item) => item.strength === "medium")) return "medium";
  return "low";
}

function evidenceReference(
  title: string,
  items: Evidence[],
  prefix: string,
) {
  return {
    title,
    explanation: `${prefix}（来源：${items.map((item) => sourceLabel(item.sourceType)).join("、")}）`,
    evidenceIds: items.map((item) => item.id),
    strength: strengthFromEvidence(items),
  };
}

export function createMockAnalysis(
  request: AnalysisRequest,
  retrievedEvidence: Evidence[],
): AnalysisResult {
  const book = getBook(request.bookId);
  if (!book) throw new Error("未找到作品");

  const hardChecks = request.hardConstraintIds.map((optionId) => {
    const option = getOption(optionId) as PreferenceOption | undefined;
    const relevant = retrievedEvidence.filter((item) => item.optionIds.includes(optionId));
    const statuses = new Set(relevant.map((item) => item.status));
    const status = statuses.has("present")
      ? "present"
      : statuses.has("conflicting")
        ? "conflicting"
        : statuses.has("possible")
          ? "possible"
          : relevant.length > 0
            ? "unknown"
            : "no_evidence";

    return {
      optionId,
      label: option?.label ?? optionId,
      status,
      evidenceIds: relevant.map((item) => item.id),
      explanation:
        status === "present"
          ? "证据显示该条件存在。"
          : status === "possible"
            ? "有相关线索，但程度或定义仍需结合读者阈值判断。"
            : status === "conflicting"
              ? "不同来源存在差异，不能给出单一确定结论。"
              : "当前证据不足，不代表该条件不存在。",
      spoilerLevel: relevant.some((item) => item.spoilerLevel === "major")
        ? "major"
        : relevant.some((item) => item.spoilerLevel === "mild")
          ? "mild"
          : "none",
    } as const;
  });

  const matchItems = retrievedEvidence.filter(
    (item) =>
      request.positivePreferenceIds.some((optionId) => item.optionIds.includes(optionId)) &&
      ["present", "possible"].includes(item.status),
  );
  const riskItems = retrievedEvidence.filter(
    (item) =>
      request.hardConstraintIds.some((optionId) => item.optionIds.includes(optionId)) &&
      ["present", "possible", "conflicting"].includes(item.status),
  );

  const unknownItems = hardChecks
    .filter((check) => ["unknown", "no_evidence", "conflicting"].includes(check.status))
    .map((check) => `${check.label}：${check.explanation}`);

  const hasConfirmedHardRisk = hardChecks.some((check) => check.status === "present");
  const hasUncertainHardRisk = hardChecks.some((check) =>
    ["possible", "conflicting", "unknown", "no_evidence"].includes(check.status),
  );
  const verdict: AnalysisResult["verdict"] = hasConfirmedHardRisk
    ? "likely_mismatch"
    : hasUncertainHardRisk
      ? "insufficient_evidence"
      : "likely_match";
  const suggestedAction: AnalysisResult["suggestedAction"] =
    verdict === "likely_mismatch" ? "exclude" : verdict === "likely_match" ? "try" : "verify";

  const result = {
    runId: crypto.randomUUID(),
    bookId: book.id,
    verdict,
    summary:
      verdict === "likely_mismatch"
        ? "至少一个已设置的硬性条件有证据显示存在，建议先排除。"
        : verdict === "insufficient_evidence"
          ? "部分条件仍无法确认，建议继续核验后再决定。"
          : "当前证据支持这些偏好，适合进入试读判断。",
    matchPoints: matchItems.length
      ? [evidenceReference("与本次偏好相关", matchItems, "部分证据与本次偏好方向一致")]
      : [],
    riskPoints: riskItems.length
      ? [evidenceReference("需要注意的风险", riskItems, "相关证据提示需要进一步关注")]
      : [],
    hardConstraintChecks: hardChecks,
    conflictingViews: retrievedEvidence.some((item) => item.status === "conflicting")
      ? [evidenceReference("存在相反或不一致的观点", retrievedEvidence.filter((item) => item.status === "conflicting"), "不同来源对相关内容的理解不完全一致")]
      : [],
    unknownItems,
    suggestedAction,
    retrievedEvidenceIds: retrievedEvidence.map((item) => item.id),
    validationFlags: ["mock_mode", "evidence_ids_checked", "unknown_not_equal_absent"],
    modelMode: "mock" as const,
  };

  return result;
}


