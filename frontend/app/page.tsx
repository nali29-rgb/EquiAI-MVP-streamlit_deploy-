"use client";

import { useState } from "react";
import { ShieldCheck, AlertTriangle, Cpu, ArrowUpRight } from "lucide-react";

export default function Dashboard() {
  const [ats, setAts] = useState("Workday Recruiting");

  return (
    <div className="min-h-screen bg-slate-50 text-brand-dark p-8 font-sans">
      {/* Top Navbar */}
      <header className="max-w-7xl mx-auto bg-white border border-slate-200 border-t-4 border-t-brand-blue rounded-2xl p-6 shadow-sm flex justify-between items-center mb-8">
        <div className="flex items-center gap-3">
          <div className="bg-brand-canvas p-2.5 rounded-xl border border-brand-blue/20">
            <ShieldCheck className="w-6 h-6 text-brand-blue" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">EquiAudit AI</h1>
            <p className="text-xs text-slate-500 font-medium">Continuous Algorithmic Compliance</p>
          </div>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-xs font-semibold border border-slate-200">
            Tenant: Acme Corp Legal Ops
          </span>
          <span className="px-3 py-1 bg-brand-coral/10 text-brand-coral rounded-full text-xs font-semibold border border-brand-coral/20">
            Live Risk Detected
          </span>
        </div>
      </header>

      {/* Main Grid Layout */}
      <main className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* Metric Cards */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 border-t-4 border-t-brand-blue shadow-sm">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Compliance Score</p>
          <h2 className="text-3xl font-extrabold text-brand-blue mt-2">84%</h2>
          <span className="inline-flex items-center text-xs font-medium text-emerald-600 mt-2">
            <ArrowUpRight className="w-3 h-3 mr-1" /> +4% vs last audit
          </span>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 border-t-4 border-t-brand-coral shadow-sm">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Legal Risk</p>
          <h2 className="text-3xl font-extrabold text-brand-coral mt-2">1 Stage</h2>
          <span className="text-xs font-semibold text-brand-coral/90 mt-2 block">
            Screening Auto-Reject
          </span>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 border-t-4 border-t-brand-coral shadow-sm">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">EEOC Impact Ratio</p>
          <h2 className="text-3xl font-extrabold text-brand-coral mt-2">0.33</h2>
          <span className="text-xs font-semibold text-red-500 mt-2 block">
            Below 0.80 Federal Parity
          </span>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 border-t-4 border-t-brand-blue shadow-sm">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Connected ATS</p>
          <h2 className="text-2xl font-bold text-slate-800 mt-2">{ats}</h2>
          <span className="text-xs font-semibold text-brand-blue mt-2 block">
            Auto-Sync Ready
          </span>
        </div>
      </main>
    </div>
  );
}