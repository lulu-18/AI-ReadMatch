"use client";

import { useMemo, useState } from "react";
import type { AnalysisResult, Book, PreferenceOption } from "@/schemas/readmatch";

type AnalyzeResponse = { result: AnalysisResult; book: Book } | { error: string };

const verdictText = {
  likely_match: "可能适合",
  likely_mismatch: "可能不适合",
  insufficient_evidence: "证据不足",
};

const actionText = {
  try: "愿意试读",
  exclude: "排除",
  verify: "继续核验",
};

const statusText = {
  present: "已发现相关条件",
  possible: "可能存在",
  conflicting: "读者观点不一致",
  unknown: "当前无法确认",
  no_evidence: "暂未找到证据",
};

export function ReadMatchApp({
  books,
  options,
}: {
  books: Book[];
  options: PreferenceOption[];
}) {
  const [bookId, setBookId] = useState(books[0]?.id ?? "");
  const [positiveIds, setPositiveIds] = useState<string[]>([]);
  const [hardIds, setHardIds] = useState<string[]>([]);
  const [optionalText, setOptionalText] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [resultBook, setResultBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const positiveOptions = useMemo(
    () => options.filter((option) => option.type === "positive"),
    [options],
  );
  const hardOptions = useMemo(
    () => options.filter((option) => option.type === "hard_constraint"),
    [options],
  );

  function toggle(id: string, values: string[], setter: (values: string[]) => void) {
    setter(values.includes(id) ? values.filter((value) => value !== id) : [...values, id]);
  }

  async function analyze() {
    setLoading(true);
    setMessage("");
    setResult(null);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          bookId,
          positivePreferenceIds: positiveIds,
          hardConstraintIds: hardIds,
          optionalText,
        }),
      });
      const data = (await response.json()) as AnalyzeResponse;
      if (!response.ok || "error" in data) throw new Error("error" in data ? data.error : "分析失败");
      setResult(data.result);
      setResultBook(data.book);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "分析失败，请稍后重试");
    } finally {
      setLoading(false);
    }
  }

  async function sendFeedback(userAction: "try" | "exclude" | "verify", helpful: boolean) {
    if (!result) return;
    const response = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ runId: result.runId, userAction, helpful, issueTypes: [], optionalText: "" }),
    });
    const data = (await response.json()) as { message?: string; error?: string };
    setMessage(data.message ?? data.error ?? "反馈已提交");
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-5 py-8 md:px-10 md:py-12">
      <header className="mb-8 grid gap-5 border-b border-stone-200 pb-8 md:grid-cols-[1.4fr_0.8fr] md:items-end">
        <div>
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.22em] text-amber-700">ReadMatch · M1 Mock</p>
          <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-stone-950 md:text-6xl">
            先看证据，再决定要不要读。
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-stone-600 md:text-lg">
            针对已收录的纯爱作品，逐项检查你的偏好和阅读边界。当前为三本样例的 Mock 模式，不会调用真实模型或自行联网。
          </p>
        </div>
        <div className="rounded-3xl bg-stone-950 p-5 text-stone-50">
          <p className="text-sm text-stone-400">产品原则</p>
          <p className="mt-2 text-lg leading-7">不为覆盖而猜，不为完整而编；帮助用户判断，不替用户决定。</p>
        </div>
      </header>

      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="rounded-3xl border border-stone-200 bg-white p-5 shadow-sm md:p-7">
          <div className="mb-6">
            <p className="text-sm font-semibold text-amber-700">01 · 选择作品</p>
            <label className="mt-3 block text-sm font-medium text-stone-700" htmlFor="book">当前精选书库</label>
            <select
              id="book"
              value={bookId}
              onChange={(event) => setBookId(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-stone-300 bg-stone-50 px-4 py-3 text-stone-950 outline-none focus:border-amber-600"
            >
              {books.map((book) => (
                <option key={book.id} value={book.id}>{book.title} · {book.author}</option>
              ))}
            </select>
          </div>

          <OptionGroup
            title="02 · 这次想看什么？"
            description="可选。没有正向偏好也可以只做雷点检查。"
            options={positiveOptions}
            selected={positiveIds}
            onToggle={(id) => toggle(id, positiveIds, setPositiveIds)}
          />

          <OptionGroup
            title="03 · 这次重点避开什么？"
            description="硬性条件会被逐项检查；暂未找到证据不等于不存在。"
            options={hardOptions}
            selected={hardIds}
            onToggle={(id) => toggle(id, hardIds, setHardIds)}
          />

          <label className="mt-6 block text-sm font-medium text-stone-700" htmlFor="optionalText">可选补充</label>
          <textarea
            id="optionalText"
            value={optionalText}
            onChange={(event) => setOptionalText(event.target.value)}
            maxLength={500}
            placeholder="例如：可以接受慢热，但不能接受长期没有关系推进。"
            className="mt-2 min-h-24 w-full resize-y rounded-2xl border border-stone-300 bg-stone-50 px-4 py-3 text-sm leading-6 outline-none focus:border-amber-600"
          />

          <button
            type="button"
            onClick={analyze}
            disabled={loading || !bookId}
            className="mt-5 w-full rounded-2xl bg-amber-700 px-5 py-3.5 font-semibold text-white transition hover:bg-amber-800 disabled:cursor-not-allowed disabled:bg-stone-400"
          >
            {loading ? "正在基于受控证据分析…" : "开始分析"}
          </button>
          {message ? <p className="mt-3 text-sm text-stone-600">{message}</p> : null}
        </div>

        <div className="min-h-[640px] rounded-3xl border border-stone-200 bg-[#f7f4ee] p-5 md:p-7">
          {result && resultBook ? (
            <ResultPanel result={result} book={resultBook} onFeedback={sendFeedback} />
          ) : (
            <div className="flex min-h-[580px] flex-col items-center justify-center rounded-2xl border border-dashed border-stone-300 px-8 text-center">
              <span className="text-5xl">📚</span>
              <h2 className="mt-5 text-2xl font-semibold text-stone-900">结果会显示在这里</h2>
              <p className="mt-3 max-w-md leading-7 text-stone-600">选择作品和本次条件后，系统会区分已确认事实、读者观点、风险和未知项。</p>
            </div>
          )}
        </div>
      </section>
    </main>
  );
}

function OptionGroup({ title, description, options, selected, onToggle }: { title: string; description: string; options: PreferenceOption[]; selected: string[]; onToggle: (id: string) => void }) {
  return (
    <fieldset className="mt-7">
      <legend className="text-sm font-semibold text-amber-700">{title}</legend>
      <p className="mt-2 text-sm leading-6 text-stone-500">{description}</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {options.map((option) => {
          const active = selected.includes(option.id);
          return (
            <button
              key={option.id}
              type="button"
              aria-pressed={active}
              title={option.description}
              onClick={() => onToggle(option.id)}
              className={`rounded-full border px-3.5 py-2 text-sm transition ${active ? "border-amber-700 bg-amber-700 text-white" : "border-stone-300 bg-white text-stone-700 hover:border-amber-500"}`}
            >
              {option.label}
            </button>
          );
        })}
      </div>
    </fieldset>
  );
}

function ResultPanel({ result, book, onFeedback }: { result: AnalysisResult; book: Book; onFeedback: (action: "try" | "exclude" | "verify", helpful: boolean) => void }) {
  return (
    <div>
      <div className="flex flex-wrap items-start justify-between gap-4 border-b border-stone-300 pb-5">
        <div>
          <p className="text-sm text-stone-500">{book.author} · {book.platform} · {book.completionStatus === "completed" ? "已完结" : "状态未知"}</p>
          <h2 className="mt-1 text-3xl font-semibold text-stone-950">《{book.title}》</h2>
        </div>
        <span className="rounded-full bg-stone-950 px-4 py-2 text-sm font-semibold text-white">{verdictText[result.verdict]}</span>
      </div>

      <p className="mt-5 text-lg leading-8 text-stone-800">{result.summary}</p>

      <ResultSection title="硬性条件检查">
        <div className="space-y-3">
          {result.hardConstraintChecks.length ? result.hardConstraintChecks.map((check) => (
            <div key={check.optionId} className="rounded-2xl bg-white p-4 shadow-sm">
              <div className="flex items-center justify-between gap-4">
                <h3 className="font-semibold text-stone-900">{check.label}</h3>
                <span className="text-xs font-semibold text-amber-800">{statusText[check.status]}</span>
              </div>
              <p className="mt-2 text-sm leading-6 text-stone-600">{check.explanation}</p>
              <p className="mt-2 text-xs text-stone-500">证据：{check.evidenceIds.length ? check.evidenceIds.join("、") : "暂无"}{check.spoilerLevel === "major" ? " · 含重大剧透，默认不展开" : ""}</p>
            </div>
          )) : <p className="text-sm text-stone-500">本次未设置硬性条件。</p>}
        </div>
      </ResultSection>

      {result.matchPoints.length ? <ResultSection title="匹配点"><ReferenceCards items={result.matchPoints} /></ResultSection> : null}
      {result.riskPoints.length ? <ResultSection title="需要注意"><ReferenceCards items={result.riskPoints} /></ResultSection> : null}
      {result.unknownItems.length ? (
        <ResultSection title="当前未知">
          <ul className="space-y-2 text-sm leading-6 text-stone-600">{result.unknownItems.map((item) => <li key={item}>• {item}</li>)}</ul>
        </ResultSection>
      ) : null}

      <div className="mt-7 rounded-2xl bg-stone-950 p-5 text-white">
        <p className="text-sm text-stone-400">建议动作</p>
        <p className="mt-1 text-2xl font-semibold">{actionText[result.suggestedAction]}</p>
        <div className="mt-4 flex flex-wrap gap-2">
          {(["try", "exclude", "verify"] as const).map((action) => (
            <button key={action} type="button" onClick={() => onFeedback(action, true)} className="rounded-full border border-stone-600 px-3 py-2 text-sm hover:border-amber-400 hover:text-amber-300">{actionText[action]}</button>
          ))}
          <button type="button" onClick={() => onFeedback(result.suggestedAction, false)} className="rounded-full border border-red-400/60 px-3 py-2 text-sm text-red-200 hover:bg-red-950">分析不准确</button>
        </div>
      </div>

      <p className="mt-4 text-xs text-stone-500">运行模式：Mock · 证据 {result.retrievedEvidenceIds.length} 条 · {result.runId}</p>
    </div>
  );
}

function ResultSection({ title, children }: { title: string; children: React.ReactNode }) {
  return <section className="mt-7"><h3 className="mb-3 text-sm font-semibold uppercase tracking-[0.16em] text-stone-500">{title}</h3>{children}</section>;
}

function ReferenceCards({ items }: { items: AnalysisResult["matchPoints"] }) {
  return <div className="space-y-3">{items.map((item) => <div key={`${item.title}-${item.evidenceIds.join("-")}`} className="rounded-2xl bg-white p-4 shadow-sm"><div className="flex justify-between gap-4"><h4 className="font-semibold text-stone-900">{item.title}</h4><span className="text-xs text-stone-500">{item.strength}</span></div><p className="mt-2 text-sm leading-6 text-stone-600">{item.explanation}</p><p className="mt-2 text-xs text-stone-500">证据：{item.evidenceIds.join("、")}</p></div>)}</div>;
}
