"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import { 
  AlertTriangle, 
  Upload, 
  ArrowUpRight, 
  Loader2,
  X,
  CheckCircle2,
  ExternalLink,
  ChevronRight,
  Info,
  Activity,
  FileCheck2,
  Layers,
  Database
} from "lucide-react";

// Official EquiAudit Logo with Next.js Optimized Image
// Official EquiAudit Logo (Bigger & Pink Background Removed via CSS Filters)
function EquiAuditLogo() {
  return (
    <div className="flex items-center gap-3 select-none">
      <Image 
        src="/logo.png" 
        alt="EquiAudit Logo" 
        width={200}
        height={70}
        priority
        className="h-16 w-auto object-contain mix-blend-multiply contrast-125 brightness-105" 
      />
      <div className="flex items-baseline">
        <span className="text-3xl font-sans tracking-tight text-slate-900 font-light">
          Equi<span className="font-bold text-slate-900">Audit</span>
        </span>
        <span className="ml-1.5 text-xs font-black text-[#6B82C1] tracking-wider uppercase bg-blue-50 px-2 py-0.5 rounded border border-blue-200/60">
          AI
        </span>
      </div>
    </div>
  );
}

// Safe Text Sanitizer: Removes Markdown & Emojis
const cleanText = (str: string): string => {
  if (!str) return "";
  return str
    .replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g, '')
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/\*(.*?)\*/g, "$1")
    .replace(/`(.*?)`/g, "$1")
    .replace(/^#+\s*/, "")
    .trim();
};

// Executive Renderer with High-Impact Font Sizing
function ExecutiveTextRenderer({ text }: { text: string }) {
  if (!text) return null;
  const lines = text.split("\n");

  return (
    <div className="space-y-4 font-sans text-slate-800 text-base leading-relaxed">
      {lines.map((line, idx) => {
        const trimmed = line.trim();
        if (!trimmed) return null;

        if (trimmed.startsWith("#")) {
          return (
            <h4 key={idx} className="text-lg font-extrabold text-slate-900 mt-5 mb-2 pb-1.5 border-b border-slate-200 flex items-center gap-2">
              <ChevronRight className="w-5 h-5 text-brand-blue shrink-0" />
              {cleanText(trimmed)}
            </h4>
          );
        }

        if (trimmed.startsWith("-") || trimmed.startsWith("*")) {
          return (
            <div key={idx} className="flex items-start gap-3 my-2 pl-1">
              <div className="w-2 h-2 rounded-full bg-brand-blue mt-2 shrink-0" />
              <p className="text-base text-slate-700 leading-relaxed font-medium">{cleanText(trimmed.replace(/^[-*]\s*/, ""))}</p>
            </div>
          );
        }

        if (/^\d+\./.test(trimmed)) {
          const num = trimmed.match(/^\d+/)?.[0];
          const rest = trimmed.replace(/^\d+\.\s*/, "");
          return (
            <div key={idx} className="flex items-start gap-3 my-2 pl-1">
              <span className="text-xs font-black text-brand-blue bg-brand-canvas px-2 py-0.5 rounded-md border border-brand-blue/20 shrink-0 mt-0.5">
                {num}
              </span>
              <p className="text-base text-slate-700 leading-relaxed font-medium">{cleanText(rest)}</p>
            </div>
          );
        }

        return (
          <p key={idx} className="text-base text-slate-700 leading-relaxed">
            {cleanText(trimmed)}
          </p>
        );
      })}
    </div>
  );
}

interface DynamicCard {
  id: string;
  title: string;
  category: string;
  keyHighlight: string;
  content: string;
}

export default function App() {
  const [selectedAts, setSelectedAts] = useState("Greenhouse");
  const [activeTab, setActiveTab] = useState("dashboard");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [rawReport, setRawReport] = useState<string | null>(null);
  const [activeModal, setActiveModal] = useState<DynamicCard | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isMounted, setIsMounted] = useState(false);

  // Persistence: Restore tab, report, and ATS state on reload
  useEffect(() => {
    setIsMounted(true);
    const savedTab = localStorage.getItem("equiaudit_tab");
    const savedReport = localStorage.getItem("equiaudit_report");
    const savedAts = localStorage.getItem("equiaudit_ats");
    if (savedTab) setActiveTab(savedTab);
    if (savedReport) setRawReport(savedReport);
    if (savedAts) setSelectedAts(savedAts);
  }, []);

  const changeTab = (tab: string) => {
    setActiveTab(tab);
    if (typeof window !== "undefined") {
      localStorage.setItem("equiaudit_tab", tab);
    }
  };

  const handleAtsChange = (ats: string) => {
    setSelectedAts(ats);
    if (typeof window !== "undefined") {
      localStorage.setItem("equiaudit_ats", ats);
    }
  };

  const handleRunAudit = async () => {
    if (!file) {
      alert("Please upload a CSV dataset first.");
      return;
    }

    setLoading(true);
    setError(null);
    setRawReport(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("target_ats", selectedAts);

    const backendUrl = process.env.NEXT_PUBLIC_API_URL || "https://equiaudit-backend.onrender.com";

    try {
      const response = await fetch(`${backendUrl}/api/audit`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setRawReport(data.report);
        if (typeof window !== "undefined") {
          localStorage.setItem("equiaudit_report", data.report);
        }
      } else {
        setError(data.error || "Execution error.");
      }
    } catch (err) {
      console.error("API Error:", err);
      setError("Backend server waking up or offline. Please retry in a few seconds.");
    } finally {
      setLoading(false);
    }
  };

  // Concise Executive Titles Mapping (Max 3-4 Words)
  const CONCISE_TITLES = [
    "1. Funnel & Impact Ratio",
    "2. Root Cause Diagnosis",
    "3. Systemic Fix Playbook",
    "4. Legal Retention Plan"
  ];

  // Parser: Separates Protocol Note and builds 2-column square cards
  const parseReport = (text: string) => {
    if (!text) return { protocolNote: null, cards: [] };

    let protocolNote: string | null = null;
    const cards: DynamicCard[] = [];

    const rawSections = text.split(/(?=^#{1,3}\s)/m).filter(s => s.trim().length > 0);

    rawSections.forEach((sec) => {
      const lines = sec.trim().split("\n");
      const rawTitle = lines[0] || "";
      const cleanedTitle = cleanText(rawTitle);
      const body = lines.slice(1).join("\n").trim();

      if (
        cleanedTitle.toLowerCase().includes("audit protocol note") || 
        sec.toLowerCase().includes("audit protocol note")
      ) {
        const fullNote = cleanText(sec);
        protocolNote = fullNote.replace(/^audit protocol note:?/i, "").trim();
      } else {
        const cardIndex = cards.length;
        const conciseTitle = CONCISE_TITLES[cardIndex] || cleanText(cleanedTitle).slice(0, 25);
        
        // Extract a strong headline snippet for immediate visual pop
        const previewSnippet = cleanText(body || sec).slice(0, 140);

        cards.push({
          id: `module-${cardIndex + 1}`,
          title: conciseTitle,
          category: `MODULE 0${cardIndex + 1}`,
          keyHighlight: previewSnippet,
          content: body || sec
        });
      }
    });

    return { protocolNote, cards };
  };

  const { protocolNote, cards } = parseReport(rawReport || "");

  if (!isMounted) return null;

  return (
    <div className="min-h-screen bg-slate-50/70 text-slate-900 font-sans antialiased selection:bg-brand-blue selection:text-white">
      {/* Header with Official Logo */}
      <header className="bg-white/90 backdrop-blur-md border-b border-slate-200/80 sticky top-0 z-40 shadow-xs">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <EquiAuditLogo />

          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 bg-slate-100/80 px-3.5 py-2 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              Tenant: <strong className="text-slate-900">Acme Legal Ops</strong>
            </div>
            <div className="bg-brand-coral/10 text-brand-coral px-3.5 py-2 rounded-xl border border-brand-coral/20 text-xs font-bold flex items-center gap-2 shadow-xs">
              <AlertTriangle className="w-4 h-4 shrink-0" /> 
              <span>1 Risk Active</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        
        {/* Navigation Tabs */}
        <div className="bg-slate-200/60 p-1.5 rounded-2xl inline-flex gap-1 mb-8 border border-slate-200 shadow-inner">
          <button
            onClick={() => changeTab("dashboard")}
            className={`px-6 py-2.5 rounded-xl font-bold text-sm transition-all duration-200 ${
              activeTab === "dashboard"
                ? "bg-white text-brand-blue shadow-md shadow-slate-200/80"
                : "text-slate-600 hover:text-slate-900 hover:bg-white/50"
            }`}
          >
            Dashboard Overview
          </button>
          <button
            onClick={() => changeTab("audit")}
            className={`px-6 py-2.5 rounded-xl font-bold text-sm transition-all duration-200 ${
              activeTab === "audit"
                ? "bg-white text-brand-blue shadow-md shadow-slate-200/80"
                : "text-slate-600 hover:text-slate-900 hover:bg-white/50"
            }`}
          >
            Execute Audit Workflow
          </button>
        </div>

        {/* TAB 1: DASHBOARD OVERVIEW */}
        {activeTab === "dashboard" ? (
          <div className="space-y-8 animate-in fade-in duration-300">
            {/* Hero Banner */}
            <div className="relative overflow-hidden bg-gradient-to-br from-white via-slate-50 to-brand-canvas/30 p-8 rounded-3xl border border-slate-200/90 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
              <div className="space-y-2 z-10 max-w-2xl">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-blue/10 text-brand-blue text-xs font-extrabold uppercase tracking-wider border border-brand-blue/20">
                  <Activity className="w-3.5 h-3.5" /> Real-Time Engine Active
                </div>
                <h2 className="text-2xl md:text-3xl font-black tracking-tight text-slate-900">
                  EEOC & Algorithmic Bias Compliance
                </h2>
                <p className="text-slate-600 text-sm font-medium leading-relaxed">
                  Continuous multi-jurisdictional monitoring across candidate screening pipelines, ATS rules, and scoring algorithms.
                </p>
              </div>

              <button 
                onClick={() => changeTab("audit")}
                className="z-10 bg-brand-blue hover:bg-slate-900 text-white font-extrabold text-sm px-6 py-3.5 rounded-2xl transition-all shadow-lg shadow-brand-blue/20 hover:shadow-xl hover:-translate-y-0.5 flex items-center gap-2 shrink-0"
              >
                Run Fresh Audit <ArrowUpRight className="w-4 h-4" />
              </button>

              <div className="absolute -right-12 -top-12 w-64 h-64 bg-brand-blue/5 rounded-full blur-3xl pointer-events-none" />
            </div>

            {/* Metric Widgets Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-3xl border-t-4 border-t-brand-blue border-x border-b border-slate-200/80 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-xs font-black uppercase tracking-wider text-slate-400">Compliance Score</span>
                  <FileCheck2 className="w-5 h-5 text-brand-blue" />
                </div>
                <div className="text-4xl font-black text-slate-900 tracking-tight">84%</div>
                <div className="flex items-center text-xs font-bold text-emerald-600 mt-3 bg-emerald-50 w-fit px-2.5 py-1 rounded-lg border border-emerald-200/60">
                  <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" /> +4% vs last audit
                </div>
              </div>

              <div className="bg-white p-6 rounded-3xl border-t-4 border-t-brand-coral border-x border-b border-slate-200/80 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-xs font-black uppercase tracking-wider text-slate-400">Active Exposure</span>
                  <AlertTriangle className="w-5 h-5 text-brand-coral" />
                </div>
                <div className="text-4xl font-black text-brand-coral tracking-tight">1 Stage</div>
                <div className="text-xs font-extrabold text-brand-coral mt-3 bg-brand-coral/10 w-fit px-2.5 py-1 rounded-lg border border-brand-coral/20">
                  Screening Auto-Reject Failure
                </div>
              </div>

              <div className="bg-white p-6 rounded-3xl border-t-4 border-t-brand-coral border-x border-b border-slate-200/80 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-xs font-black uppercase tracking-wider text-slate-400">EEOC Impact Ratio</span>
                  <Layers className="w-5 h-5 text-brand-coral" />
                </div>
                <div className="text-4xl font-black text-slate-900 tracking-tight">0.33</div>
                <div className="text-xs font-extrabold text-red-600 mt-3 bg-red-50 w-fit px-2.5 py-1 rounded-lg border border-red-200/60">
                  Below 0.80 Federal Parity
                </div>
              </div>

              <div className="bg-white p-6 rounded-3xl border-t-4 border-t-brand-blue border-x border-b border-slate-200/80 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-xs font-black uppercase tracking-wider text-slate-400">Active ATS</span>
                  <Database className="w-5 h-5 text-brand-blue" />
                </div>
                <div className="text-2xl font-black text-slate-900 tracking-tight mt-1">{selectedAts}</div>
                <div className="text-xs font-extrabold text-brand-blue mt-3 bg-brand-canvas w-fit px-2.5 py-1 rounded-lg border border-brand-blue/20">
                  Auto-Sync Enabled
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* TAB 2: AUDIT WORKFLOW */
          <div className="space-y-8 animate-in fade-in duration-300">
            {/* Upload Card */}
            <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm">
              <h3 className="text-xl font-extrabold text-slate-900 mb-1">Trigger Algorithmic Audit</h3>
              <p className="text-sm font-medium text-slate-500 mb-6">
                Select applicant tracking system and upload candidate dataset to calculate disparate impact metrics for <span className="font-extrabold text-brand-blue">{selectedAts}</span>.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-xs font-black text-slate-700 uppercase tracking-wider mb-2">ATS Platform</label>
                  <select
                    value={selectedAts}
                    onChange={(e) => handleAtsChange(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-2xl p-3.5 text-sm font-bold text-slate-800 focus:ring-2 focus:ring-brand-blue outline-none"
                  >
                    <option value="Greenhouse">Greenhouse</option>
                    <option value="Workday Recruiting">Workday Recruiting</option>
                    <option value="Lever">Lever</option>
                    <option value="SmartRecruiters">SmartRecruiters</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-black text-slate-700 uppercase tracking-wider mb-2">Upload Candidate Dataset (CSV)</label>
                  <div className="relative border-2 border-dashed border-slate-300 bg-slate-50 rounded-2xl p-4 text-center hover:bg-brand-canvas/30 transition-all cursor-pointer">
                    <input
                      type="file"
                      accept=".csv"
                      onChange={(e) => setFile(e.target.files?.[0] || null)}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <Upload className="w-5 h-5 text-brand-blue mx-auto mb-1" />
                    <span className="text-xs font-bold text-slate-700 block">
                      {file ? `Selected: ${file.name}` : "Click to upload CSV dataset"}
                    </span>
                  </div>
                </div>
              </div>

              {error && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-600 rounded-2xl text-xs font-bold">
                  {error}
                </div>
              )}

              <button
                onClick={handleRunAudit}
                disabled={loading}
                className="w-full bg-brand-blue hover:bg-slate-900 text-white font-extrabold text-base py-4 rounded-2xl transition-all shadow-md shadow-brand-blue/20 flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Executing Compliance Engine for {selectedAts}...
                  </>
                ) : (
                  `Execute Algorithmic Audit for ${selectedAts}`
                )}
              </button>
            </div>

            {/* Audit Results Section */}
            {rawReport && (
              <div className="space-y-6">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-6 h-6 text-emerald-500 shrink-0" />
                  <h4 className="text-xl font-black text-slate-900 tracking-tight">Audit Results & Executive Action Items</h4>
                </div>

                {/* Top Written Protocol Banner */}
                {protocolNote && (
                  <div className="bg-gradient-to-r from-brand-canvas/60 via-white to-brand-canvas/30 border border-brand-blue/25 rounded-2xl p-6 flex items-start gap-4 shadow-sm">
                    <Info className="w-6 h-6 text-brand-blue shrink-0 mt-0.5" />
                    <div className="space-y-1">
                      <h5 className="text-xs font-black text-brand-blue uppercase tracking-wider">Audit Protocol Notice</h5>
                      <p className="text-sm font-semibold text-slate-800 leading-relaxed">
                        {protocolNote}
                      </p>
                    </div>
                  </div>
                )}

                {/* 2-Column Square Cards Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {cards.map((card) => (
                    <div
                      key={card.id}
                      onClick={() => setActiveModal(card)}
                      className="bg-white p-7 rounded-3xl border-2 border-slate-200 hover:border-brand-blue hover:shadow-xl transition-all duration-200 cursor-pointer group flex flex-col justify-between min-h-[220px]"
                    >
                      <div>
                        {/* Header Badge */}
                        <div className="flex justify-between items-center mb-3">
                          <span className="text-xs font-black text-brand-blue uppercase tracking-widest bg-brand-canvas px-3 py-1 rounded-lg border border-brand-blue/20">
                            {card.category}
                          </span>
                          <span className="text-xs font-extrabold px-3 py-1 rounded-lg bg-slate-100 text-slate-700 border border-slate-200">
                            Action
                          </span>
                        </div>

                        {/* Concise Heading */}
                        <h5 className="text-xl font-black text-slate-900 group-hover:text-brand-blue transition-colors leading-snug mb-3">
                          {card.title}
                        </h5>

                        {/* Main Highlight */}
                        <p className="text-sm font-semibold text-slate-600 leading-relaxed line-clamp-3">
                          {card.keyHighlight}...
                        </p>
                      </div>

                      {/* Footer Callout */}
                      <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs font-extrabold text-brand-blue">
                        <span className="text-xs tracking-wide">Click to open full breakdown</span>
                        <ExternalLink className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Pop-up Modal */}
      {activeModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl border border-slate-200 max-w-2xl w-full p-8 shadow-2xl space-y-6 animate-in fade-in zoom-in-95">
            <div className="flex justify-between items-start border-b border-slate-100 pb-4">
              <div>
                <span className="text-xs font-black text-brand-blue uppercase tracking-widest bg-brand-canvas px-3 py-1 rounded-lg border border-brand-blue/20">
                  {activeModal.category}
                </span>
                <h3 className="text-xl font-black text-slate-900 mt-3">{activeModal.title}</h3>
              </div>
              <button
                onClick={() => setActiveModal(null)}
                className="p-2 rounded-xl hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="bg-slate-50/80 p-6 rounded-2xl border border-slate-200 max-h-[60vh] overflow-y-auto">
              <ExecutiveTextRenderer text={activeModal.content} />
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setActiveModal(null)}
                className="bg-brand-blue text-white px-7 py-3 rounded-2xl text-sm font-extrabold hover:bg-slate-900 transition-all shadow-md"
              >
                Close Details
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
