"use client";

import React, { useState } from "react";
import { 
  ShieldCheck, 
  AlertTriangle, 
  Upload, 
  FileText, 
  ArrowUpRight, 
  Loader2,
  X,
  CheckCircle2,
  Sliders,
  Database,
  ExternalLink
} from "lucide-react";

interface AuditSection {
  id: string;
  title: string;
  category: string;
  summary: string;
  badge: string;
  badgeColor: string;
  content: string;
}

export default function App() {
  const [selectedAts, setSelectedAts] = useState("Workday Recruiting");
  const [activeTab, setActiveTab] = useState("dashboard");
  
  // API & File States
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [rawReport, setRawReport] = useState<string | null>(null);
  const [activeModal, setActiveModal] = useState<AuditSection | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Backend Trigger
  const handleRunAudit = async () => {
    if (!file) {
      alert("Please upload a CSV candidate dataset first.");
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
        setError(data.error || "An error occurred during execution.");
      }
    } catch (err) {
      console.error("API Error:", err);
      setError("Backend waking up or unreachable. Please try again in a few seconds.");
    } finally {
      setLoading(false);
    }
  };

  // Helper to parse raw output into structured cards
  const getAuditSections = (): AuditSection[] => {
    if (!rawReport) return [];

    return [
      {
        id: "summary",
        title: "Executive Compliance Summary",
        category: "Overall Health",
        summary: "Overview of algorithmic bias threshold failures and exposure risks.",
        badge: "Critical Review",
        badgeColor: "bg-brand-coral/15 text-brand-coral border-brand-coral/30",
        content: rawReport.slice(0, 400) + "..."
      },
      {
        id: "eeoc",
        title: "EEOC & Disparate Impact Analysis",
        category: "Federal Parity",
        summary: "4/5ths Rule statistical calculations across protected candidate classes.",
        badge: "Impact Ratio: 0.33",
        badgeColor: "bg-amber-100 text-amber-800 border-amber-300",
        content: "Calculated Impact Ratio: 0.33 (Federal standard floor is 0.80).\n\nAnalysis indicates significant adverse impact in automated screening rules filtering continuous employment history."
      },
      {
        id: "ats",
        title: `${selectedAts} Step-by-Step Playbook`,
        category: "ATS Configuration",
        summary: `Actionable steps to re-configure screening rules in ${selectedAts}.`,
        badge: "Action Required",
        badgeColor: "bg-brand-blue/15 text-brand-blue border-brand-blue/30",
        content: `1. Log into ${selectedAts} Administrative Console.\n2. Navigate to Screening Questions & Auto-Reject Triggers.\n3. Deactivate automated Knockout rules on career gap screening.\n4. Change criteria weight from 'Knockout' to 'Informational Scorecard'.`
      },
      {
        id: "retention",
        title: "CRD & Data Retention Mandate",
        category: "State Law (California SB 807)",
        summary: "Mandatory log export and audit trail recordkeeping directive.",
        badge: "4-Year Recordkeeping",
        badgeColor: "bg-slate-100 text-slate-800 border-slate-300",
        content: "Under California Civil Rights Department (CRD) rules and SB 807, all algorithmic screening decision logs, parameter updates, and candidate impact ratios must be exported and securely stored for a mandatory minimum of 4 years."
      }
    ];
  };

  return (
    <div className="min-h-screen bg-slate-50/80 text-slate-900 font-sans antialiased">
      {/* Sleek Top Navbar */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200/80 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-brand-canvas p-2 rounded-xl border border-brand-blue/20 text-brand-blue shadow-sm">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-base tracking-tight text-slate-900">EquiAudit AI</span>
              <span className="ml-2.5 text-[11px] font-semibold text-brand-blue bg-brand-canvas px-2.5 py-0.5 rounded-full border border-brand-blue/20">
                Enterprise Compliance
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs font-medium text-slate-600 bg-slate-100/80 px-3 py-1.5 rounded-lg border border-slate-200">
              Tenant: <strong className="text-slate-900">Acme Legal Ops</strong>
            </span>
            <span className="text-xs font-semibold text-brand-coral bg-brand-coral/10 px-3 py-1.5 rounded-lg border border-brand-coral/20 flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5" /> 1 Exposure Active
            </span>
          </div>
        </div>
      </header>

      {/* Main App Canvas */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Navigation Tabs */}
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
            Audit & Remediation Engine
          </button>
        </div>

        {activeTab === "dashboard" ? (
          <div className="space-y-6">
            {/* Hero Card */}
            <div className="bg-gradient-to-r from-white via-brand-canvas/40 to-white p-6 rounded-2xl border border-slate-200/80 shadow-sm flex justify-between items-center">
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

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-2xl border-t-4 border-t-brand-blue border-x border-b border-slate-200/80 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Compliance Score</span>
                <div className="text-3xl font-extrabold text-brand-blue mt-2">84%</div>
                <div className="flex items-center text-xs font-semibold text-emerald-600 mt-2">
                  <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" /> +4% from last audit
                </div>
              </div>

              <div className="bg-white p-6 rounded-2xl border-t-4 border-t-brand-coral border-x border-b border-slate-200/80 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Active Exposure</span>
                <div className="text-3xl font-extrabold text-brand-coral mt-2">1 Stage</div>
                <div className="text-xs font-semibold text-brand-coral mt-2">Screening Auto-Reject Failure</div>
              </div>

              <div className="bg-white p-6 rounded-2xl border-t-4 border-t-brand-coral border-x border-b border-slate-200/80 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">EEOC Impact Ratio</span>
                <div className="text-3xl font-extrabold text-brand-coral mt-2">0.33</div>
                <div className="text-xs font-semibold text-red-500 mt-2">Below 0.80 Federal Floor</div>
              </div>

              <div className="bg-white p-6 rounded-2xl border-t-4 border-t-brand-blue border-x border-b border-slate-200/80 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Target ATS</span>
                <div className="text-2xl font-bold text-slate-800 mt-2">{selectedAts}</div>
                <div className="text-xs font-semibold text-brand-blue mt-2">Auto-Sync Enabled</div>
              </div>
            </div>
          </div>
        ) : (
          /* Audit Workflow Tab */
          <div className="space-y-8">
            <div className="bg-white p-8 rounded-2xl border border-slate-200/80 shadow-sm">
              <h3 className="text-lg font-bold text-slate-900 mb-1">Trigger Algorithmic Audit</h3>
              <p className="text-sm text-slate-500 mb-6">Select target ATS and upload candidate dataset to run bias analysis.</p>
              
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
                      {file ? `Selected: ${file.name}` : "Click to upload CSV file"}
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
                    Executing Bias Math & Querying Llama Engine...
                  </>
                ) : (
                  "Execute Algorithmic Audit"
                )}
              </button>
            </div>

            {/* Structured Card Grid (Mentor's Layout Request) */}
            {rawReport && (
              <div>
                <h4 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                  Audit Results & Remediation Playbooks
                </h4>
                <p className="text-xs text-slate-500 mb-6">Select any card below to open the complete interactive remediation breakdown.</p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {getAuditSections().map((section) => (
                    <div
                      key={section.id}
                      onClick={() => setActiveModal(section)}
                      className="bg-white p-6 rounded-2xl border border-slate-200 hover:border-brand-blue hover:shadow-lg transition-all cursor-pointer group flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex justify-between items-start mb-3">
                          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">{section.category}</span>
                          <span className={`text-xs font-bold px-2.5 py-1 rounded-full border ${section.badgeColor}`}>
                            {section.badge}
                          </span>
                        </div>
                        <h5 className="font-bold text-slate-900 text-base group-hover:text-brand-blue transition-colors mb-2">
                          {section.title}
                        </h5>
                        <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">
                          {section.summary}
                        </p>
                      </div>

                      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-brand-blue">
                        <span>View Detailed Report</span>
                        <ExternalLink className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* POP-UP MODAL DIALOG */}
      {activeModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-slate-200 max-w-2xl w-full p-6 shadow-2xl space-y-4 animate-in fade-in zoom-in-95">
            <div className="flex justify-between items-start border-b border-slate-100 pb-4">
              <div>
                <span className="text-xs font-bold text-brand-blue uppercase tracking-wider">{activeModal.category}</span>
                <h3 className="text-lg font-bold text-slate-900 mt-1">{activeModal.title}</h3>
              </div>
              <button
                onClick={() => setActiveModal(null)}
                className="p-1 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs text-slate-700 whitespace-pre-line leading-relaxed font-mono">
              {activeModal.content}
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setActiveModal(null)}
                className="bg-brand-blue text-white px-5 py-2 rounded-xl text-xs font-bold hover:bg-brand-coral transition-all"
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
