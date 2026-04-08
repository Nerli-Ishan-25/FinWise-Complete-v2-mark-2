import { createContext, useContext, useState, useEffect, useCallback, useMemo } from "react"
import {
  dashboardAPI, transactionAPI, assetAPI, loanAPI,
  liabilityAPI, budgetAPI, categoryAPI,
  subscriptionAPI, insightsAPI,
} from "../services/api"
import api from "../services/api"
import { useAuth } from "./AuthContext"

const FinanceContext = createContext()

export function FinanceProvider({ children }) {
  const { user, isAuthenticated } = useAuth()

  const [dashboard,     setDashboard]     = useState(null)
  const [transactions,  setTransactions]  = useState([])
  const [assets,        setAssets]        = useState([])
  const [liabilities,   setLiabilities]   = useState([])
  const [loans,         setLoans]         = useState([])
  const [budgets,       setBudgets]       = useState([])
  const [categories,    setCategories]    = useState([])
  const [subscriptions, setSubscriptions] = useState([])
  const [insights,      setInsights]      = useState(null)
  const [loading,       setLoading]       = useState(false)
  const [toast,         setToast]         = useState(null)   // { message, type }

  // ── Derived values ────────────────────────────────────────────────────────
  const monthlyIncome    = dashboard?.monthlyIncome   ?? 0
  const monthlyExpenses  = dashboard?.monthlyExpenses ?? 0
  const savingsRate      = dashboard?.savingsRate     ?? 0
  const healthScore      = dashboard?.financialHealthScore ?? 0
  const totalAssets      = assets.reduce((s, a) => s + (a.value  || 0), 0)
  const totalLiabilities = liabilities.reduce((s, l) => s + (l.amount || 0), 0)
  // Always compute netWorth locally so it instantly reflects CRUD changes
  const netWorth         = totalAssets - totalLiabilities

  // ── Toast helpers ─────────────────────────────────────────────────────────
  function showToast(message, type = "error") {
    setToast({ message, type })
  }
  function clearToast() { setToast(null) }

  // ── Chart Data ────────────────────────────────────────────────────────────
  const monthlyTrends = useMemo(() => {
    const MAP = {}
    transactions.forEach(tx => {
      const d   = new Date(tx.date)
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`
      const m   = d.toLocaleString("default", { month: "short" })
      if (!MAP[key]) MAP[key] = { m, income: 0, expense: 0, _key: key }
      if (tx.type === "income") MAP[key].income += tx.amount
      else MAP[key].expense += tx.amount
    })
    return Object.values(MAP)
      .sort((a, b) => a._key.localeCompare(b._key))
      .slice(-7)
      .map(({ _key, ...rest }) => rest)
  }, [transactions])

  const CATEGORY_COLORS = {
    Housing:"#448aff", Food:"#00e676", Transport:"#ffab40",
    Subscriptions:"#b388ff", Entertainment:"#ff5252",
    Health:"#40c4ff", Income:"#64ffda", Other:"#ff80ab",
  }
  const spendingByCategory = useMemo(() => {
    const MAP = {}
    transactions.filter(tx => tx.type === "expense").forEach(tx => {
      const cat = tx.category || "Other"
      MAP[cat] = (MAP[cat] || 0) + tx.amount
    })
    return Object.entries(MAP).map(([name, value]) => ({
      name, value: parseFloat(value.toFixed(2)),
      color: CATEGORY_COLORS[name] || "#9e9e9e",
    }))
  }, [transactions])

  const netWorthHistory = useMemo(() => {
    if (monthlyTrends.length === 0) return []
    const current = totalAssets - totalLiabilities
    const result = []
    let running = current
    const reversed = [...monthlyTrends].reverse()
    reversed.forEach(m => {
      result.unshift({ m: m.m, val: Math.max(0, Math.round(running)) })
      running -= (m.income - m.expense)
    })
    return result
  }, [monthlyTrends, totalAssets, totalLiabilities])

  // ── Loaders ───────────────────────────────────────────────────────────────
  const loadDashboard     = useCallback(async () => { try { const { data } = await dashboardAPI.getMetrics();    setDashboard(data)     } catch(e){ console.error(e) } }, [])
  const loadTransactions  = useCallback(async () => { try { const { data } = await transactionAPI.list(100);     setTransactions(data)  } catch(e){ console.error(e) } }, [])
  const loadAssets        = useCallback(async () => { try { const { data } = await assetAPI.list();              setAssets(data)        } catch(e){ console.error(e) } }, [])
  const loadLiabilities   = useCallback(async () => { try { const { data } = await liabilityAPI.list();          setLiabilities(data)   } catch(e){ console.error(e) } }, [])
  const loadLoans         = useCallback(async () => { try { const { data } = await loanAPI.list();               setLoans(data)         } catch(e){ console.error(e) } }, [])
  const loadBudgets       = useCallback(async () => { try { const { data } = await budgetAPI.list();             setBudgets(data)       } catch(e){ console.error(e) } }, [])
  const loadCategories    = useCallback(async () => { try { const { data } = await categoryAPI.list();           setCategories(data)    } catch(e){ console.error(e) } }, [])
  const loadSubscriptions = useCallback(async () => { try { const { data } = await subscriptionAPI.list();       setSubscriptions(data) } catch(e){ console.error(e) } }, [])
  const loadInsights      = useCallback(async () => { try { const { data } = await insightsAPI.get();            setInsights(data)      } catch(e){ console.error(e) } }, [])

  useEffect(() => {
    if (!isAuthenticated) return
    // If user is not onboarded, we don't need to load all this yet (or it might be empty)
    // But once they are onboarded, we definitely want to load it.
    if (!user?.onboarded) return

    setLoading(true)
    Promise.all([
      loadDashboard(), loadTransactions(), loadAssets(),
      loadLiabilities(), loadLoans(), loadBudgets(),
      loadCategories(), loadSubscriptions(), loadInsights(),
    ]).finally(() => setLoading(false))
  }, [isAuthenticated, user?.onboarded])

  // ── Transactions ──────────────────────────────────────────────────────────
  async function addTransaction(tx) {
    try {
      if (tx.type === "income") await transactionAPI.addIncome({ amount: tx.amount, source: tx.name, date: tx.date })
      else await transactionAPI.addExpense({ amount: tx.amount, category: tx.category, description: tx.name, date: tx.date })
      // Cascade: expense affects budget utilisation AND dashboard metrics
      await Promise.all([loadTransactions(), loadDashboard(), loadBudgets()])
      showToast("Transaction saved", "success")
    } catch(e) { showToast("Failed to add transaction") }
  }

  async function deleteTransaction(id) {
    try {
      await api.delete(`/finance/transactions/${id}`)
      // Cascade: deleted transaction affects budget utilisation AND dashboard
      await Promise.all([loadTransactions(), loadDashboard(), loadBudgets()])
    }
    catch(e) { showToast("Failed to delete transaction") }
  }

  // ── Assets ────────────────────────────────────────────────────────────────
  async function addAsset(asset) {
    try {
      await assetAPI.create({ name: asset.name, type: asset.type, value: parseFloat(asset.value) })
      await Promise.all([loadAssets(), loadDashboard()])
      showToast("Asset added", "success")
    } catch(e) { showToast("Failed to add asset") }
  }
  async function deleteAsset(id) {
    try {
      await assetAPI.delete(id)
      await Promise.all([loadAssets(), loadDashboard()])
    } catch(e) { showToast("Failed to delete asset") }
  }
  async function updateAsset(id, asset) {
    try {
      await assetAPI.update(id, { name: asset.name, type: asset.type, value: parseFloat(asset.value) })
      await Promise.all([loadAssets(), loadDashboard()])
      showToast("Asset updated", "success")
    } catch(e) { showToast("Failed to update asset") }
  }

  // ── Liabilities ───────────────────────────────────────────────────────────
  async function addLiability(lib) {
    try {
      await liabilityAPI.create({ name: lib.name, type: lib.type || "Other", amount: parseFloat(lib.amount), interest_rate: parseFloat(String(lib.interest_rate ?? lib.apr ?? 0).replace("%","")) || 0 })
      await Promise.all([loadLiabilities(), loadDashboard()])
      showToast("Liability added", "success")
    } catch(e) { showToast("Failed to add liability") }
  }
  async function deleteLiability(id) {
    try {
      await liabilityAPI.delete(id)
      await Promise.all([loadLiabilities(), loadDashboard()])
    } catch(e) { showToast("Failed to delete liability") }
  }
  async function updateLiability(id, liability) {
    try {
      await liabilityAPI.update(id, { name: liability.name, type: liability.type || "Other", amount: parseFloat(liability.amount), interest_rate: parseFloat(String(liability.interest_rate).replace("%","")) || 0 })
      await Promise.all([loadLiabilities(), loadDashboard()])
      showToast("Liability updated", "success")
    } catch(e) { showToast("Failed to update liability") }
  }

  // ── Loans ─────────────────────────────────────────────────────────────────
  async function addLoan(loan) {
    try {
      await loanAPI.create({ loan_amount: parseFloat(loan.loan_amount), interest_rate: parseFloat(loan.interest_rate), remaining_amount: parseFloat(loan.loan_amount) })
      await loadLoans(); showToast("Loan saved", "success")
    } catch(e) { showToast("Failed to save loan") }
  }
  async function deleteLoan(id) {
    try { await loanAPI.delete(id); await loadLoans() }
    catch(e) { showToast("Failed to delete loan") }
  }

  // ── Budgets ───────────────────────────────────────────────────────────────
  async function addBudgetCategory(cat) {
    try {
      const { data: newCat } = await categoryAPI.create({ name: cat.category, type: "expense" })
      const now = new Date()
      await budgetAPI.create({ category_id: newCat.id, budget_amount: parseFloat(cat.budget), month: now.getMonth() + 1, year: now.getFullYear() })
      await Promise.all([loadBudgets(), loadCategories()]); showToast("Budget category added", "success")
    } catch(e) { showToast("Failed to add budget category") }
  }
  async function deleteBudgetCategory(id) {
    try { await budgetAPI.delete(id); await loadBudgets() }
    catch(e) { showToast("Failed to delete budget") }
  }
  async function updateBudgetCategory(id, budget) {
    try {
      await budgetAPI.update(id, { budget_amount: parseFloat(budget.budget) })
      await Promise.all([loadBudgets(), loadDashboard()])
      showToast("Budget updated", "success")
    } catch(e) { showToast("Failed to update budget") }
  }

  // ── Subscriptions ─────────────────────────────────────────────────────────
  async function addSubscription(sub) {
    try { await subscriptionAPI.create(sub); await loadSubscriptions(); showToast("Subscription added", "success") }
    catch(e) { showToast("Failed to add subscription") }
  }
  async function deleteSubscription(id) {
    try { await subscriptionAPI.delete(id); await loadSubscriptions() }
    catch(e) { showToast("Failed to delete subscription") }
  }
  async function updateSubscription(id, data) {
    try { await subscriptionAPI.update(id, data); await loadSubscriptions() }
    catch(e) { showToast("Failed to update subscription") }
  }

  return (
    <FinanceContext.Provider value={{
      dashboard, transactions, assets, liabilities, loans, budgets, categories, subscriptions, insights,
      netWorth, monthlyIncome, monthlyExpenses, savingsRate, healthScore, totalAssets, totalLiabilities,
      monthlyTrends, spendingByCategory, netWorthHistory,
      loading, toast, clearToast,
      addTransaction, deleteTransaction,
      addAsset, deleteAsset, updateAsset,
      addLiability, deleteLiability, updateLiability,
      addLoan, deleteLoan,
      addBudgetCategory, deleteBudgetCategory, updateBudgetCategory,
      addSubscription, deleteSubscription, updateSubscription,
      loadDashboard, loadTransactions, loadBudgets, loadInsights,
    }}>
      {children}
    </FinanceContext.Provider>
  )
}

export const useFinance = () => useContext(FinanceContext)
