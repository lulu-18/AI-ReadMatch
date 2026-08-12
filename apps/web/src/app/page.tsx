import { ReadMatchApp } from "@/components/readmatch-app";
import { listActiveBooks, listPreferenceOptions } from "@/domain/repositories/catalog";

export default function Home() {
  return <ReadMatchApp books={listActiveBooks()} options={listPreferenceOptions()} />;
}
