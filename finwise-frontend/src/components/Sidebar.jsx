import { NavLink, useNavigate } from "react-router-dom"
import {
  LayoutDashboard, TrendingUp, Calculator,
  Receipt, CreditCard, Lightbulb, Sparkles, Settings, LogOut, User
} from "lucide-react"
import { useFinance } from "../context/FinanceContext"
import { useAuth }    from "../context/AuthContext"

const NAV = [
  { to: "/",          icon: LayoutDashboard, label: "Dashboard"      },
  { to: "/net-worth", icon: TrendingUp,      label: "Net Worth"      },
  { to: "/budget",    icon: Calculator,      label: "Budget Planner" },
  { to: "/expenses",  icon: Receipt,         label: "Expenses"       },
  { to: "/loans",     icon: CreditCard,      label: "Loans"          },
  { to: "/insights",  icon: Lightbulb,       label: "Insights"       },
  { to: "/assistant", icon: Sparkles,        label: "AI Assistant"   },
]

export default function Sidebar() {
  const { netWorth, loading } = useFinance()
  const { user, logout }      = useAuth()
  const navigate              = useNavigate()

  function handleLogout() { logout(); navigate("/login") }
  const fmt = (n) => "$" + Math.abs(n).toLocaleString("en-US", { minimumFractionDigits: 0 })

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">$</div>
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
            <Icon />{label}
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
