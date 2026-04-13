import { NavLink, useNavigate } from "react-router-dom"
import dashboardIcon from "../assets/icons/nav-icons/nav-dashboard.svg"
import networthIcon from "../assets/icons/nav-icons/nav-networth.svg"
import budgetIcon from "../assets/icons/nav-icons/nav-budget.svg"
import expensesIcon from "../assets/icons/nav-icons/nav-expenses.svg"
import loansIcon from "../assets/icons/nav-icons/nav-loans.svg"
import insightsIcon from "../assets/icons/nav-icons/nav-insights.svg"
import assistantIcon from "../assets/icons/nav-icons/nav-ai-assistant.svg"
import appLogo from "../assets/icons/app-logo/logo-pulse-hex.svg"

import { Settings, LogOut, User } from "lucide-react"
import { useFinance } from "../context/FinanceContext"
import { useAuth }    from "../context/AuthContext"

const NAV = [
  { to: "/",          icon: dashboardIcon, label: "Dashboard"      },
  { to: "/net-worth", icon: networthIcon,  label: "Net Worth"      },
  { to: "/budget",    icon: budgetIcon,    label: "Budget Planner" },
  { to: "/expenses",  icon: expensesIcon,  label: "Expenses"       },
  { to: "/loans",     icon: loansIcon,     label: "Loans"          },
  { to: "/insights",  icon: insightsIcon,  label: "Insights"       },
  { to: "/assistant", icon: assistantIcon, label: "AI Assistant"   },
]

export default function Sidebar() {
  const { netWorth, loading } = useFinance()
  const { user, logout }      = useAuth()
  const navigate              = useNavigate()

  function handleLogout() { logout(); navigate("/login") }
  const { formatCurrency, currencySymbol } = useFinance()
  const fmt = (n) => formatCurrency(n)

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <img src={appLogo} alt="FinWise Logo" style={{ width: 32, height: 32, marginRight: 8 }} />
        <div className="logo-text">
          <h2>FinWise</h2>
          <p>AI Finance</p>
        </div>
      </div>

      <div className="net-worth-widget">
        <div className="label">Net Worth</div>
        <div className="amount">{loading ? "..." : fmt(netWorth)}</div>
        <div className="change" style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <User size={10} />
          {user?.name || "My Account"}
        </div>
      </div>

      <nav>
        {NAV.map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to} end={to === "/"} className={({ isActive }) => isActive ? "active" : ""}>
            <img src={Icon} alt={label} style={{ width: 20, height: 20, marginRight: 8, filter: "var(--icon-filter, none)" }} />{label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <NavLink to="/settings" className={({ isActive }) => isActive ? "active" : ""}>
          <Settings /> Settings
        </NavLink>
        <button type="button" onClick={handleLogout}>
          <LogOut /> Log Out
        </button>
      </div>
    </aside>
  )
}
