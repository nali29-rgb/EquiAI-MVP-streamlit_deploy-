"use client";

import React, { useState } from "react";
import { 
  ShieldCheck, 
  AlertTriangle, 
  Upload, 
  ArrowUpRight, 
  Loader2,
  X,
  CheckCircle2,
  ExternalLink,
  ChevronRight,
  Info
} from "lucide-react";

// Safe Sanitizer: Removes Markdown AND emojis (compatible with Next.js SWC build target)
const cleanText = (str: string): string => {
  if (!str) return "";
  return str
    // Standard Emoji Stripper
    .replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g, '')
    // Markdown Stripper
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/\*(.*?)\*/g, "$1")
    .replace(/`(.*?)`/g, "$1")
    .replace(/^#+\s*/, "")
    .trim();
};

// Executive Renderer for Modal Pop-up Content
function ExecutiveTextRenderer({ text }: { text: string }) {
  if (!text) return null;

  const lines = text.split("\n");

  return (
    <div className="space-y-3 font-sans text-slate-700 text-sm leading-relaxed">
      {lines.map((line, idx) => {
        const trimmed = line.trim();
        if (!trimmed) return null;

        if (trimmed.startsWith("#")) {
          return (
            <h4 key={idx} className="text-sm font-bold text-slate-900 mt-4 mb-2 pb-1 border-b border-slate-200 flex items-center gap-2">
              <ChevronRight className="w-4 h-4 text-brand-blue" />
              {cleanText(trimmed)}
            </h4>
          );
        }

        if (trimmed.startsWith("-") || trimmed.startsWith("*")) {
          return (
            <div key={idx} className="flex items-start gap-2.5 my-1.5 pl-1">
              <div className="w-1.5 h-1.5 rounded-full bg-brand-blue mt-2 shrink-0" />
              <p className="text-xs text-slate-700 leading-normal">{cleanText(trimmed.replace(/^[-*]\s*/, ""))}</p>
            </div>
          );
        }

        if (/^\d+\./.test(trimmed)) {
          const num = trimmed.match(/^\d+/)?.[0];
          const rest = trimmed.replace(/^\d+\.\s*/, "");
          return (
            <div key={idx} className="flex items-start gap-2.5 my-1.5 pl-1">
              <span className="text-[10px] font-bold text-brand-blue bg-brand-canvas px-1.5 py-0.5 rounded border border-brand-blue/20 shrink-0 mt-0.5">
                {num}
              </span>
              <p className="text-xs text-slate-700 leading-normal">{cleanText(rest)}</p>
            </div>
          );
        }

        return (
          <p key={idx} className="text-xs text-slate-600 leading-relaxed">
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
  content: string;
}

export default function App() {
  const [selectedAts, setSelectedAts] = useState("Workday Recruiting");
  const [activeTab, setActiveTab] = useState("dashboard");
  
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [rawReport, setRawReport] = useState<string | null>(null);
  const [activeModal, setActiveModal] = useState<DynamicCard | null>(null);
  const [error, setError] = useState<string | null>(null);

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

  // Parser: Separates Protocol Note to top banner and creates concise cards
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
        cards.push({
          id: `sec-${cards.length + 1}`,
          title: cleanedTitle || `Compliance Module ${cards.length + 1}`,
          category: `MODULE 0${cards.length + 1}`,
          content: body || sec
        });
      }
    });

    return { protocolNote, cards };
  };

  const { protocolNote, cards } = parseReport(rawReport || "");

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans antialiased">
      {/* SaaS Top Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-brand-canvas p-2 rounded-xl border border-brand-blue/20 text-brand-blue">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-base tracking-tight text-slate-900">EquiAudit AI</span>
              <span className="ml-2.5 text-[11px] font-semibold text-brand-blue bg-brand-canvas px-2.5 py-0.5 rounded-full border border-brand-blue/20">
                Enterprise Engine
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs font-medium text-slate-600 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
              Tenant: <strong className="text-slate-900">Acme Legal Ops</strong>
            </span>
            <span className="text-xs font-semibold text-brand-coral bg-brand-coral/10 px-3 py-1.5 rounded-lg border border-brand-coral/20 flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5" /> 1 Risk Detected
            </span>
          </div>
        </div>
      </header>

      {/* Main Canvas */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex gap-2 border-b border-slate-200 mb-8 pb-1">
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
              activeTab === "dashboard"
                ? "bg-brand-blue text-white shadow-md shadow-brand-blue/20"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            Dashboard Overview
          </button>
          <button
            onClick={() => setActiveTab("audit")}
            className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
              activeTab === "audit"
                ? "bg-brand-blue text-white shadow-md shadow-brand-blue/20"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            Execute Audit Workflow
          </button>
        </div>

        {activeTab === "dashboard" ? (
          <div className="space-y-6">
            <div className="bg-gradient-to-r from-white via-brand-canvas/30 to-white p-6 rounded-2xl border border-slate-200 shadow-sm flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-slate-900">EEOC & Algorithmic Bias Compliance</h2>
                <p className="text-sm text-slate-500 mt-1">Real-time risk monitoring across active candidate screening funnels.</p>
              </div>
              <button 
                onClick={() => setActiveTab("audit")}
                className="bg-brand-blue hover:bg-brand-coral text-white font-semibold text-sm px-5 py-2.5 rounded-xl transition-all shadow-sm"
              >
                Run Fresh Audit
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-2xl border-t-4 border-t-brand-blue border-x border-b border-slate-200 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Compliance Score</span>
                <div className="text-3xl font-extrabold text-brand-blue mt-2">84%</div>
                <div className="flex items-center text-xs font-semibold text-emerald-600 mt-2">
                  <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" /> +4% vs last audit
                </div>
              </div>

              <div className="bg-white p-6 rounded-2xl border-t-4 border-t-brand-coral border-x border-b border-slate-200 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Active Risk</span>
                <div className="text-3xl font-extrabold text-brand-coral mt-2">1 Stage</div>
                <div className="text-xs font-semibold text-brand-coral mt-2">Screening Auto-Reject Failure</div>
              </div>

              <div className="bg-white p-6 rounded-2xl border-t-4 border-t-brand-coral border-x border-b border-slate-200 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">EEOC Impact Ratio</span>
                <div className="text-3xl font-extrabold text-brand-coral mt-2">0.33</div>
                <div className="text-xs font-semibold text-red-500 mt-2">Below 0.80 Federal Parity</div>
              </div>

              <div className="bg-white p-6 rounded-2xl border-t-4 border-t-brand-blue border-x border-b border-slate-200 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Target ATS</span>
                <div className="text-2xl font-bold text-slate-800 mt-2">{selectedAts}</div>
                <div className="text-xs font-semibold text-brand-blue mt-2">Auto-Sync Enabled</div>
              </div>
            </div>
          </div>
        ) : (
          /* Audit Workflow Tab */
          <div className="space-y-8">
            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
              <h3 className="text-lg font-bold text-slate-900 mb-1">Trigger Algorithmic Audit</h3>
              <p className="text-sm text-slate-500 mb-6">Select target ATS platform and upload applicant dataset to run bias analysis.</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Target ATS Platform</label>
                  <select
                    value={selectedAts}
                    onChange={(e) => setSelectedAts(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-xl p-3 text-sm font-semibold text-slate-800 focus:ring-2 focus:ring-brand-blue outline-none"
                  >
                    <option>Workday Recruiting</option>
                    <option>Greenhouse</option>
                    <option>Lever</option>
                    <option>SmartRecruiters</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Upload Candidate Dataset (CSV)</label>
                  <div className="relative border-2 border-dashed border-slate-300 bg-slate-50 rounded-xl p-4 text-center hover:bg-brand-canvas/20 transition-all cursor-pointer">
                    <input
                      type="file"
                      accept=".csv"
                      onChange={(e) => setFile(e.target.files?.[0] || null)}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <Upload className="w-5 h-5 text-brand-blue mx-auto mb-1" />
                    <span className="text-xs font-semibold text-slate-600 block">
                      {file ? `Selected: ${file.name}` : "Click to upload CSV dataset"}
                    </span>
                  </div>
                </div>
              </div>

              {error && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-600 rounded-xl text-xs font-semibold">
                  {error}
                </div>
              )}

              <button
                onClick={handleRunAudit}
                disabled={loading}
                className="w-full bg-brand-blue hover:bg-brand-coral text-white font-bold py-3.5 rounded-xl transition-all shadow-md shadow-brand-blue/20 flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Running Compliance Engine...
                  </>
                ) : (
                  "Execute Algorithmic Audit"
                )}
              </button>
            </div>

            {/* Audit Results Container */}
            {rawReport && (
              <div className="space-y-6">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                  <h4 className="text-base font-bold text-slate-900">Audit Results & Remediation Cards</h4>
                </div>

                {/* 1. TOP WRITTEN BANNER */}
                {protocolNote && (
                  <div className="bg-brand-canvas/40 border border-brand-blue/20 rounded-2xl p-5 flex items-start gap-3 shadow-sm">
                    <Info className="w-5 h-5 text-brand-blue shrink-0 mt-0.5" />
                    <div className="space-y-1">
                      <h5 className="text-xs font-bold text-brand-blue uppercase tracking-wider">Audit Protocol Notice</h5>
                      <p className="text-xs text-slate-700 font-medium leading-relaxed">
                        {protocolNote}
                      </p>
                    </div>
                  </div>
                )}

                {/* 2. CONCISE CARDS GRID */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                  {cards.map((card) => (
                    <div
                      key={card.id}
                      onClick={() => setActiveModal(card)}
                      className="bg-white p-5 rounded-2xl border border-slate-200 hover:border-brand-blue hover:shadow-md transition-all cursor-pointer group flex flex-col justify-between h-36"
                    >
                      <div>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">{card.category}</span>
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                            Action
                          </span>
                        </div>
                        <h5 className="font-bold text-slate-900 text-sm group-hover:text-brand-blue transition-colors leading-snug line-clamp-2">
                          {card.title}
                        </h5>
                      </div>

                      <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-brand-blue">
                        <span className="text-[11px]">View breakdown</span>
                        <ExternalLink className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
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
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-slate-200 max-w-2xl w-full p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-start border-b border-slate-100 pb-4">
              <div>
                <span className="text-xs font-bold text-brand-blue uppercase tracking-wider">{activeModal.category}</span>
                <h3 className="text-base font-bold text-slate-900 mt-1">{activeModal.title}</h3>
              </div>
              <button
                onClick={() => setActiveModal(null)}
                className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="bg-slate-50/80 p-5 rounded-xl border border-slate-200/80 max-h-[60vh] overflow-y-auto">
              <ExecutiveTextRenderer text={activeModal.content} />
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setActiveModal(null)}
                className="bg-brand-blue text-white px-5 py-2.5 rounded-xl text-xs font-bold hover:bg-brand-coral transition-all shadow-sm"
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
