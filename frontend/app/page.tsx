// Exact Logo using the high-res image asset
function EquiAuditLogo() {
  return (
    <div className="flex items-center gap-3 select-none">
      {/* Real Image Asset */}
      <img 
        src="/logo.png" 
        alt="EquiAudit Logo" 
        className="h-10 w-auto object-contain mix-blend-multiply" 
      />
      {/* Brand Typography */}
      <div className="flex items-baseline">
        <span className="text-2xl font-sans tracking-tight text-slate-900 font-light">
          Equi<span className="font-bold text-slate-900">Audit</span>
        </span>
        <span className="ml-1.5 text-[10px] font-black text-[#6B82C1] tracking-wider uppercase bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200/60">
          AI
        </span>
      </div>
    </div>
  );
}
