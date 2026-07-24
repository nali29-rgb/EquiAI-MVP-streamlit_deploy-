"use client";

import React, { useState } from "react";
import { 
  ShieldCheck, 
  AlertTriangle, 
  Upload, 
  FileText, 
  ArrowUpRight, 
  Loader2
} from "lucide-react";

export default function App() {
  const [selectedAts, setSelectedAts] = useState("Workday Recruiting");
  const [activeTab, setActiveTab] = useState("dashboard");
  
  // API Integration States
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [auditResult, setAuditResult] = useState<{ metrics: any; report: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Live Backend Connection Function
  const handleRunAudit = async () => {
    if (!file) {
      alert("Please upload a CSV dataset before running the audit.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("target_ats", selectedAts);

    // Fallback to Render URL or use process.env value
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || "https://equiaudit-backend.onrender.com";

    try {
      const response = await fetch(`${backendUrl}/api/audit`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setAuditResult(data);
      } else {
        setError(data.error || "An error occurred during audit execution.");
      }
    } catch (err) {
      console.error("API Error:", err);
      setError("Failed to connect to backend engine. Ensure Render service is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Top SaaS Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-brand-canvas p-2 rounded-xl border border-brand-blue/30 text-brand-blue">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight text-slate-900">EquiAudit AI</span>
              <span className="ml-2 text-xs font-semibold text-brand-blue bg-brand-canvas px-2.5 py-0.5 rounded-full border border-brand-blue/20">
                Continuous Compliance Engine
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs font-medium text-slate-500 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
              Tenant: <strong className="text-slate-800">Acme Legal Ops</strong>
            </span>
            <span className="text-xs font-semibold text-brand-coral bg-brand-coral/10 px-3 py-1.5 rounded-lg border border-brand-coral/20 flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5" /> 1 Active Exposure
            </span>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Navigation Tabs */}
        <div className="flex gap-2 border-b border-slate-200 mb-8 pb-1">
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`px-4 py-2.5 rounded-lg font-semibold text-sm transition-all ${
              activeTab === "dashboard"
                ? "bg-brand-blue text-white shadow-md shadow-brand-blue/20"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            Dashboard Overview
          </button>
          <button
            onClick={() => setActiveTab("audit")}
            className={`px-4 py-2.5 rounded-lg font-semibold text-sm transition-all ${
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
            {/* Hero Card */}
            <div className="bg-gradient-to-r from-white via-brand-canvas/30 to-white p-6 rounded-2xl border border-brand-blue/20 shadow-sm flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-slate-900">EEOC & Algorithmic Bias Compliance</h2>
                <p className="text-sm text-slate-500 mt-1">Real-time risk monitoring across active candidate screening funnels.</p>
              </div>
              <button 
                onClick={() => setActiveTab("audit")}
                className="bg-brand-blue hover:bg-brand-coral text-white font-semibold text-sm px-5 py-2.5 rounded-xl transition-all shadow-md"
              >
                Run Fresh Audit
              </button>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-2xl border-t-4 border-t-brand-blue border-x border-b border-slate-200 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Compliance Score</span>
                <div className="text-3xl font-extrabold text-brand-blue mt-2">84%</div>
                <div className="flex items-center text-xs font-semibold text-emerald-600 mt-2">
                  <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" /> +4% from last quarter
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
                <div className="text-xs font-semibold text-red-500 mt-2">Below 0.80 Federal Standard</div>
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
          <div className="space-y-6">
            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
              <h3 className="text-lg font-bold text-slate-900 mb-2">Configure & Trigger Bias Audit</h3>
              <p className="text-sm text-slate-500 mb-6">Select your target ATS platform and upload applicant data to trigger Llama compliance reasoning.</p>
              
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
                    <Upload className="w-6 h-6 text-brand-blue mx-auto mb-1" />
                    <span className="text-xs font-semibold text-slate-600 block">
                      {file ? `Selected: ${file.name}` : "Click to upload or drag & drop CSV file"}
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
                    Executing Bias Math Engine & Querying Llama...
                  </>
                ) : (
                  "Run Algorithmic Engine & Generate Playbook"
                )}
              </button>
            </div>

            {/* Audit Results Output */}
            {auditResult && (
              <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center gap-2 pb-4 border-b border-slate-100">
                  <FileText className="w-5 h-5 text-brand-blue" />
                  <h4 className="font-bold text-slate-900">Compliance & Remediation Report</h4>
                </div>
                <div className="prose prose-slate max-w-none text-sm whitespace-pre-line leading-relaxed text-slate-800">
                  {auditResult.report}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
