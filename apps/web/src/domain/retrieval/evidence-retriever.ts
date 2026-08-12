import type { Evidence } from "@/schemas/readmatch";
import { listEvidenceForBook } from "@/domain/repositories/catalog";

export function retrieveEvidence(
  bookId: string,
  optionIds: string[],
): Evidence[] {
  const bookEvidence = listEvidenceForBook(bookId);
  if (optionIds.length === 0) return bookEvidence;

  const matched = bookEvidence.filter((item) =>
    item.optionIds.some((optionId) => optionIds.includes(optionId)),
  );

  return matched.length > 0 ? matched : bookEvidence;
}
