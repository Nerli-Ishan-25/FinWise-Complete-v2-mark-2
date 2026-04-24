import { useState } from "react"
import { CreditCard, Activity, Save, Trash2, AlertCircle } from "lucide-react"
import { useFinance } from "../context/FinanceContext"
import { loanAssessmentAPI } from "../services/api"

// Approximate Indian bank home loan rates (FY 2025 — for reference only)
const LENDERS = [
  { name: "Bank of Baroda",    type: "PSU",     rate: 8.40, stars: 4, best: true  },
  { name: "SBI",               type: "PSU",     rate: 8.50, stars: 5, best: false },
  { name: "Kotak Mahindra",    type: "Private", rate: 8.65, stars: 4, best: false },
  { name: "HDFC Bank",         type: "Private", rate: 8.75, stars: 5, best: false },
  { name: "Axis Bank",         type: "Private", rate: 8.75, stars: 4, best: false },
  { name: "ICICI Bank",        type: "Private", rate: 8.85, stars: 4, best: false },
]

function Stars({ n }) {
  return <div className="stars">{"★".repeat(n)}{"☆".repeat(5 - n)}</div>
}

function calcMonthly(principal, ratePct, termMonths) {
  const r = ratePct / 100 / 12
  const n = termMonths
  if (r === 0) return principal / n
  return (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1)
}

export default function Loans() {
  const { loans, addLoan, deleteLoan, formatCurrency, currencySymbol } = useFinance()

  const [form, setForm] = useState({ 
    amount: "20000", rate: "7", term: "60", loanPurpose: "Home",
    age: "35", income: "60000", debt: "800", creditScore: "680", 
    monthsEmployed: "48", numCreditLines: "3", education: "Bachelor's", 
    employmentType: "Full-time", maritalStatus: "Single",
    hasMortgage: "No", hasDependents: "No", hasCoSigner: "No"
  })
  
  const [result,  setResult]  = useState(null)
  const [loading, setLoading] = useState(false)
  const [saving,  setSaving]  = useState(false)
  const [error,   setError]   = useState(null)

  async function analyze() {
    setLoading(true)
    setError(null)
    
    try {
      const principal = parseFloat(form.amount)
      const monthlyPmt = calcMonthly(principal, parseFloat(form.rate), parseFloat(form.term))

      const annualIncome = parseFloat(form.income)
      const monthlyIncome = annualIncome / 12
      const existingDebt = parseFloat(form.debt)
      // DTI is computed server-side from income + existing_debt
      const dtiRatio = (existingDebt + monthlyPmt) / monthlyIncome   // local-only, for display

      const payload = {
        age: parseInt(form.age),
        income: annualIncome,
        credit_score: parseInt(form.creditScore),
        months_employed: parseInt(form.monthsEmployed),
        num_credit_lines: parseInt(form.numCreditLines),
        education: form.education,
        employment_type: form.employmentType,
        marital_status: form.maritalStatus,
        has_mortgage: form.hasMortgage,
        has_dependents: form.hasDependents,
        has_co_signer: form.hasCoSigner,
        loan_amount: principal,
        loan_term: parseInt(form.term),
        existing_debt: existingDebt,
        loan_purpose: form.loanPurpose
      }

      const res = await loanAssessmentAPI.predict(payload)
      const data = res.data

      const n = parseFloat(form.term)
      const totalInt = monthlyPmt * n - principal

      setResult({ 
        monthly: monthlyPmt, 
        totalInt, 
        dti: dtiRatio * 100, 
        risk: data.risk_level,
        riskColor: data.risk_level === "Low" ? "var(--green)" : data.risk_level === "Moderate" ? "var(--amber)" : "var(--red)",
        ai: data
      })
    } catch (err) {
      if (err.response?.data?.detail) {
        setError(JSON.stringify(err.response.data.detail))
      } else {
        setError(err.message)
      }
    } finally {
      setLoading(false)
    }
  }

  async function handleSaveLoan() {
    if (!result) return
    setSaving(true)
    await addLoan({ loan_amount: form.amount, interest_rate: form.rate, remaining_amount: form.amount })
    setSaving(false)
  }

  const lendersWithPayment = LENDERS.map(l => {
    if (!result) return { ...l, monthly: null, total: null }
    const principal = parseFloat(form.amount)
    const n = parseFloat(form.term)
    const m = calcMonthly(principal, l.rate, n)
    return { ...l, monthly: m, total: m * n }
  })

  // Helper for inputs
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <div className="eyebrow">XGBoost AI Verification</div>
          <h1>Loan Analyzer</h1>
        </div>
      </div>

      {error && (
        <div className="alert-bar danger" style={{ marginBottom: 20 }}>
          <AlertCircle size={16} /> {error}
        </div>
      )}

      <div className="grid-2-1" style={{ marginBottom: 20 }}>
        {/* Input Form */}
        <div className="chart-card">
          <div className="chart-title" style={{ marginBottom: 16 }}><CreditCard size={16} /> New Loan Request</div>
          <div className="form-grid" style={{ marginBottom: 24 }}>
            <div className="input-group">
              <label>Loan Amount ({currencySymbol})</label>
              <input className="input-field" type="number" name="amount" value={form.amount} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label>Interest Rate (%)</label>
              <input className="input-field" type="number" step="0.1" name="rate" value={form.rate} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label>Term (months)</label>
              <input className="input-field" type="number" name="term" value={form.term} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label>Purpose</label>
              <select className="input-field" name="loanPurpose" value={form.loanPurpose} onChange={handleChange}>
                <option>Home</option><option>Auto</option><option>Business</option><option>Education</option><option>Other</option>
              </select>
            </div>
          </div>

          <div className="chart-title" style={{ marginBottom: 16 }}><Activity size={16} /> Applicant Profile</div>
          <div className="form-grid" style={{ marginBottom: 24 }}>
            <div className="input-group">
              <label>Age</label>
              <input className="input-field" type="number" name="age" value={form.age} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label>Credit Score</label>
              <input className="input-field" type="number" name="creditScore" value={form.creditScore} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label>Annual Income ({currencySymbol})</label>
              <input className="input-field" type="number" name="income" value={form.income} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label>Existing Debt/month ({currencySymbol})</label>
              <input className="input-field" type="number" name="debt" value={form.debt} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label>Open Credit Lines</label>
              <input className="input-field" type="number" name="numCreditLines" value={form.numCreditLines} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label>Months Employed</label>
              <input className="input-field" type="number" name="monthsEmployed" value={form.monthsEmployed} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label>Employment</label>
              <select className="input-field" name="employmentType" value={form.employmentType} onChange={handleChange}>
                <option>Full-time</option><option>Part-time</option><option>Self-employed</option><option>Unemployed</option>
              </select>
            </div>
            <div className="input-group">
              <label>Education</label>
              <select className="input-field" name="education" value={form.education} onChange={handleChange}>
                <option>High School</option><option>Bachelor's</option><option>Master's</option><option>PhD</option>
              </select>
            </div>
            <div className="input-group">
              <label>Marital Status</label>
              <select className="input-field" name="maritalStatus" value={form.maritalStatus} onChange={handleChange}>
                <option>Single</option><option>Married</option><option>Divorced</option>
              </select>
            </div>
            <div className="input-group">
              <label>Has Mortgage</label>
              <select className="input-field" name="hasMortgage" value={form.hasMortgage} onChange={handleChange}><option>Yes</option><option>No</option></select>
            </div>
            <div className="input-group">
              <label>Has Dependents</label>
              <select className="input-field" name="hasDependents" value={form.hasDependents} onChange={handleChange}><option>Yes</option><option>No</option></select>
            </div>
            <div className="input-group">
              <label>Co-Signer</label>
              <select className="input-field" name="hasCoSigner" value={form.hasCoSigner} onChange={handleChange}><option>Yes</option><option>No</option></select>
            </div>
          </div>

          <div style={{ display: "flex", gap: 10 }}>
            <button className="btn btn-primary" style={{ flex: 1, justifyContent: "center" }}
              onClick={analyze} disabled={loading}>
              <Activity size={14} /> {loading ? "Analyzing via AI..." : "Analyze Affordability"}
            </button>
            {result && (
              <button className="btn btn-outline" onClick={handleSaveLoan} disabled={saving}
                title="Save this loan to history">
                <Save size={14} /> {saving ? "Saving..." : "Save Loan"}
              </button>
            )}
          </div>
        </div>

        {/* Risk Assessment */}
        <div className="chart-card">
          <div className="chart-title">◎ Risk Assessment</div>
          {!result ? (
            <div style={{ color: "var(--text-secondary)", fontSize: 13, lineHeight: 1.7, padding: "20px 0", textAlign: "center" }}>
              Fill in the 15 data points and click<br />
              <strong style={{ color: "var(--text-primary)" }}>Analyze Affordability</strong><br />
              to dispatch the request to the XGBoost inference engine.
            </div>
          ) : (
            <div className="risk-card">
              <div className="risk-payment">{formatCurrency(result.monthly)}</div>
              <div className="risk-label">Estimated Monthly Payment</div>
              
              <div style={{ marginBottom: 10 }}>
                <span className={`badge ${result.risk === "Low" ? "badge-green" : result.risk === "Moderate" ? "badge-amber" : "badge-red"}`}>
                  {result.risk} Default Risk ({result.ai.default_probability_pct}%)
                </span>
              </div>

              <div className="risk-metrics">
                <div className="risk-metric">
                  <div className="val" style={{ color: result.riskColor }}>{result.dti.toFixed(1)}%</div>
                  <div className="key">Debt-to-Income</div>
                </div>
                <div className="risk-metric">
                  <div className="val" style={{ color: "var(--red)" }}>{formatCurrency(result.totalInt)}</div>
                  <div className="key">Total Interest</div>
                </div>
              </div>
              
              <div className="alert-bar" style={{ marginTop: 16, textAlign: "left", fontSize: 13, background: "var(--surface)", border: `1px solid ${result.riskColor}`, color: "var(--text-primary)" }}>
                <strong>AI Verdict:</strong> {result.ai.explanation}
              </div>

              {result.ai.key_factors?.length > 0 && (
                <div style={{ marginTop: 16, fontSize: 13, textAlign: "left" }}>
                  <div style={{ fontWeight: 600, color: "var(--text-secondary)", marginBottom: 8 }}>Key ML Factors:</div>
                  <ul style={{ paddingLeft: 20, margin: 0, color: "var(--text-primary)" }}>
                    {result.ai.key_factors.map((f, i) => <li key={i} style={{ marginBottom: 4 }}>{f}</li>)}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Lender Comparison */}
      <div className="chart-card" style={{ marginBottom: 20 }}>
        <div className="chart-title">📈 Lender Comparison
          <span style={{ fontSize: 11, fontWeight: 400, color: "var(--text-secondary)", marginLeft: 8 }}>
            Indicative rates · FY 2025
          </span>
        </div>
        <table className="fin-table">
          <thead>
            <tr><th>Lender</th><th>Type</th><th>Interest Rate</th><th>Est. Monthly</th><th>Total Cost</th><th>Rating</th></tr>
          </thead>
          <tbody>
            {lendersWithPayment.map(l => (
              <tr key={l.name}>
                <td>
                  <div style={{ fontWeight: 600 }}>{l.name}</div>
                  {l.best && <span className="best-rate">Best Rate</span>}
                </td>
                <td>
                  <span style={{
                    fontSize: 11, padding: "2px 7px", borderRadius: 4, fontWeight: 600,
                    background: l.type === "PSU" ? "rgba(59,130,246,0.15)" : "rgba(168,85,247,0.15)",
                    color: l.type === "PSU" ? "#60a5fa" : "#c084fc"
                  }}>{l.type}</span>
                </td>
                <td style={{ color: l.best ? "var(--green)" : "var(--text-primary)" }}>{l.rate}%</td>
                <td>{l.monthly ? formatCurrency(l.monthly) : "—"}</td>
                <td>{l.total   ? formatCurrency(l.total)   : "—"}</td>
                <td><Stars n={l.stars} /></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ fontSize: 11, color: "var(--text-secondary)", marginTop: 10, paddingTop: 8, borderTop: "1px solid var(--border)" }}>
          ⚠️ Rates shown are approximate indicative figures for FY 2025 based on publicly available data. Actual rates depend on credit profile, loan amount, and bank policy. Always verify with the lender.
        </div>
      </div>

      {/* Saved Loans History */}
      {loans.length > 0 && (
        <div className="chart-card">
          <div className="chart-title">🗂 Saved Loans</div>
          <table className="fin-table">
            <thead>
              <tr><th>Loan Amount</th><th>Interest Rate</th><th>Remaining</th><th>Saved On</th><th></th></tr>
            </thead>
            <tbody>
              {loans.map(l => (
                <tr key={l.id}>
                  <td style={{ fontWeight: 600 }}>{formatCurrency(l.loan_amount)}</td>
                  <td>{l.interest_rate}%</td>
                  <td>{formatCurrency(l.remaining_amount)}</td>
                  <td style={{ color: "var(--text-secondary)", fontSize: 12 }}>
                    {new Date(l.created_at).toLocaleDateString()}
                  </td>
                  <td>
                    <button className="btn-danger" onClick={() => deleteLoan(l.id)}>
                      <Trash2 size={12} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
