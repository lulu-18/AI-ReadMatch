import { z } from "zod";

export const spoilerLevelSchema = z.enum(["none", "mild", "major"]);
export const evidenceStrengthSchema = z.enum(["low", "medium", "high"]);
export const evidenceStatusSchema = z.enum([
  "present",
  "possible",
  "conflicting",
  "unknown",
  "no_evidence",
]);

export const bookSchema = z.object({
  id: z.string(),
  title: z.string(),
  author: z.string(),
  platform: z.string(),
  completionStatus: z.enum(["completed", "ongoing", "unknown"]),
  genre: z.string(),
  subgenres: z.array(z.string()),
  officialSourceRef: z.string().url(),
  catalogStatus: z.enum(["draft", "review", "active", "retired"]),
});

export const preferenceOptionSchema = z.object({
  id: z.string(),
  label: z.string(),
  category: z.enum([
    "character",
    "relationship",
    "romance",
    "pacing",
    "style",
    "emotion",
    "ending",
    "warning",
    "setting",
  ]),
  type: z.enum(["positive", "hard_constraint"]),
  description: z.string(),
});

export const evidenceSchema = z.object({
  id: z.string(),
  bookId: z.string(),
  sourceType: z.enum([
    "official",
    "publisher_summary",
    "reader_review",
    "reader_summary",
  ]),
  sourceRef: z.string().url(),
  summary: z.string(),
  aspect: z.enum([
    "character",
    "relationship",
    "style",
    "pacing",
    "emotion",
    "plot_logic",
    "ending",
    "warning",
    "setting",
    "status",
  ]),
  optionIds: z.array(z.string()),
  status: evidenceStatusSchema,
  spoilerLevel: spoilerLevelSchema,
  strength: evidenceStrengthSchema,
  humanReviewed: z.boolean(),
});

export const analysisRequestSchema = z.object({
  bookId: z.string().min(1),
  positivePreferenceIds: z.array(z.string()).default([]),
  hardConstraintIds: z.array(z.string()).default([]),
  optionalText: z.string().max(500).default(""),
});

export const evidenceReferenceSchema = z.object({
  evidenceIds: z.array(z.string()).min(1),
  title: z.string(),
  explanation: z.string(),
  strength: evidenceStrengthSchema,
});

export const hardConstraintCheckSchema = z.object({
  optionId: z.string(),
  label: z.string(),
  status: evidenceStatusSchema,
  evidenceIds: z.array(z.string()),
  explanation: z.string(),
  spoilerLevel: spoilerLevelSchema,
});

export const analysisResultSchema = z.object({
  runId: z.string(),
  bookId: z.string(),
  verdict: z.enum([
    "likely_match",
    "likely_mismatch",
    "insufficient_evidence",
  ]),
  summary: z.string(),
  matchPoints: z.array(evidenceReferenceSchema),
  riskPoints: z.array(evidenceReferenceSchema),
  hardConstraintChecks: z.array(hardConstraintCheckSchema),
  conflictingViews: z.array(evidenceReferenceSchema),
  unknownItems: z.array(z.string()),
  suggestedAction: z.enum(["try", "exclude", "verify"]),
  retrievedEvidenceIds: z.array(z.string()),
  validationFlags: z.array(z.string()),
  modelMode: z.literal("mock"),
});

export const feedbackRequestSchema = z.object({
  runId: z.string(),
  userAction: z.enum(["try", "exclude", "verify"]).optional(),
  helpful: z.boolean().optional(),
  issueTypes: z.array(z.string()).default([]),
  optionalText: z.string().max(500).default(""),
});

export type Book = z.infer<typeof bookSchema>;
export type PreferenceOption = z.infer<typeof preferenceOptionSchema>;
export type Evidence = z.infer<typeof evidenceSchema>;
export type AnalysisRequest = z.infer<typeof analysisRequestSchema>;
export type AnalysisResult = z.infer<typeof analysisResultSchema>;
export type FeedbackRequest = z.infer<typeof feedbackRequestSchema>;
