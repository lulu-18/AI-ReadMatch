import type { AnalysisRequest, AnalysisResult, Evidence } from "@/schemas/readmatch";
import { createMockAnalysis } from "@/domain/models/mock-provider";

export interface ModelProvider {
  readonly mode: "mock" | "openai";
  analyze(request: AnalysisRequest, evidence: Evidence[]): Promise<AnalysisResult>;
}

const mockProvider: ModelProvider = {
  mode: "mock",
  async analyze(request, evidence) {
    return createMockAnalysis(request, evidence);
  },
};

export function getModelProvider(): ModelProvider {
  const mode = process.env.READMATCH_MODEL_MODE ?? "mock";

  if (mode === "mock") return mockProvider;

  throw new Error(
    "当前仅启用 Mock 模式。获得 API Key 后再实现 OpenAIProvider，不允许静默回退到自由联网回答。",
  );
}
