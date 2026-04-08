import { Trash2 } from "lucide-react"

export default function TransactionItem({ tx, onDelete }) {
  const isIncome = tx.type === "income"
  return (
    <div className="tx-item">
      <div className="tx-icon" style={{ background: isIncome ? "rgba(0,230,118,0.1)" : "rgba(255,255,255,0.05)" }}>
        {tx.icon || "💰"}
      </div>
      <div className="tx-info">
        <div className="tx-name">{tx.name}</div>
        <div className="tx-sub">{tx.category} · {tx.date}</div>
      </div>
      <span className={`tx-amount ${isIncome ? "income" : "expense"}`}>
        {isIncome ? "+" : "-"}${tx.amount.toFixed(2)}
      </span>
      {onDelete && (
        <button className="btn-danger" onClick={() => onDelete(tx.id)} style={{ marginLeft: 8 }}>
          <Trash2 size={12} />
        </button>
      )}
    </div>
  )
}
