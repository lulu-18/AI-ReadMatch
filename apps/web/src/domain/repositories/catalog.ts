import booksJson from "@/data/books.json";
import evidenceJson from "@/data/evidence.json";
import optionsJson from "@/data/preference-options.json";
import {
  bookSchema,
  evidenceSchema,
  preferenceOptionSchema,
  type Book,
  type Evidence,
  type PreferenceOption,
} from "@/schemas/readmatch";

const books = bookSchema.array().parse(booksJson) satisfies Book[];
const evidence = evidenceSchema.array().parse(evidenceJson) satisfies Evidence[];
const options = preferenceOptionSchema.array().parse(optionsJson) satisfies PreferenceOption[];

export function listActiveBooks(): Book[] {
  return books.filter((book) => book.catalogStatus === "active");
}

export function getBook(bookId: string): Book | undefined {
  return books.find((book) => book.id === bookId);
}

export function listPreferenceOptions(): PreferenceOption[] {
  return options;
}

export function getOption(optionId: string): PreferenceOption | undefined {
  return options.find((option) => option.id === optionId);
}

export function listEvidenceForBook(bookId: string): Evidence[] {
  return evidence.filter((item) => item.bookId === bookId);
}
