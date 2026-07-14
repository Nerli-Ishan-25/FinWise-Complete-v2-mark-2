/**
 * markdownRenderer.jsx
 *
 * Lightweight, purpose-built renderer for the subset of markdown
 * the AI assistant produces. Not a general-purpose parser.
 *
 * Supported syntax:
 *   **bold**          — inline bold
 *   **Heading**\n    — standalone bold line treated as a section heading
 *   — item / - item  — unordered list item
 *   ⚠️ text          — warning callout (amber)
 *   ✅ text          — success callout (green)
 *   blank line       — vertical spacing
 */

// Splits a string on **bold** markers and returns mixed text/strong nodes
function renderInline(text) {
  const parts = text.split(/\*\*(.*?)\*\*/g)
  return parts.map((part, i) =>
    i % 2 === 1
      ? <strong key={i} style={{ color: "#f0f4ff", fontWeight: 600 }}>{part}</strong>
      : <span key={i}>{part}</span>
  )
}

export function MarkdownRenderer({ text }) {
  const lines = text.split("\n")
  const elements = []

  let inTable = false
  let tableRows = []

  const renderTable = (rows, keyIndex) => {
    // skip the separator row like |---|---|
    const validRows = rows.filter(r => !/^[|\-\s:]+$/.test(r))
    if (validRows.length === 0) return null
    return (
      <div key={`table-${keyIndex}`} style={{ overflowX: "auto", margin: "10px 0", borderRadius: 6, border: "1px solid rgba(255,255,255,0.1)" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13, color: "#c8d8f0" }}>
          <tbody>
            {validRows.map((row, rIdx) => {
              const cells = row.split("|").slice(1, -1).map(c => c.trim())
              return (
                <tr key={rIdx} style={{ borderBottom: rIdx === validRows.length - 1 ? "none" : "1px solid rgba(255,255,255,0.1)" }}>
                  {cells.map((cell, cIdx) => (
                    <td key={cIdx} style={{ padding: "8px 12px", verticalAlign: "top", borderRight: cIdx === cells.length - 1 ? "none" : "1px solid rgba(255,255,255,0.1)", background: rIdx === 0 ? "rgba(255,255,255,0.02)" : "transparent", fontWeight: rIdx === 0 ? 600 : 400 }}>
                      {renderInline(cell)}
                    </td>
                  ))}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    )
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    
    // Check for table row
    if (line.trim().startsWith("|") && line.trim().endsWith("|")) {
      inTable = true
      tableRows.push(line.trim())
      continue
    } else if (inTable) {
      elements.push(renderTable(tableRows, i))
      inTable = false
      tableRows = []
    }

    // Blank line → spacer
    if (!line.trim()) {
      elements.push(<div key={`spacer-${i}`} style={{ height: 8 }} />)
      continue
    }

    // Standalone bold heading  e.g.  **March 2026 — Overview**
    if (/^\*\*[^*]+\*\*$/.test(line.trim())) {
      elements.push(
        <div
          key={`heading-${i}`}
          style={{
            fontFamily:   "'Syne', sans-serif",
            fontWeight:   700,
            fontSize:     13,
            color:        "#f0f4ff",
            marginTop:    elements.length > 0 ? 14 : 0,
            marginBottom: 4,
            letterSpacing: "0.01em",
          }}
        >
          {line.replace(/\*\*/g, "")}
        </div>
      )
      continue
    }

    // Warning callout  ⚠️ …
    if (line.startsWith("⚠️")) {
      elements.push(
        <div
          key={`warn-${i}`}
          style={{
            margin:     "10px 0",
            padding:    "10px 14px",
            background: "rgba(255,171,64,0.1)",
            border:     "1px solid rgba(255,171,64,0.25)",
            borderRadius: 8,
            fontSize:   12.5,
            lineHeight: 1.6,
            color:      "#f0f4ff",
          }}
        >
          {renderInline(line)}
        </div>
      )
      continue
    }

    // Success callout  ✅ …
    if (line.startsWith("✅")) {
      elements.push(
        <div
          key={`success-${i}`}
          style={{
            margin:     "10px 0",
            padding:    "10px 14px",
            background: "rgba(0,230,118,0.08)",
            border:     "1px solid rgba(0,230,118,0.2)",
            borderRadius: 8,
            fontSize:   12.5,
            lineHeight: 1.6,
            color:      "#f0f4ff",
          }}
        >
          {line}
        </div>
      )
      continue
    }

    // List item  — text  or  - text
    if (line.startsWith("—") || line.startsWith("- ")) {
      elements.push(
        <div
          key={`list-${i}`}
          style={{
            display:    "flex",
            gap:        8,
            marginBottom: 3,
            paddingLeft: 4,
            fontSize:   13,
            lineHeight: 1.6,
            color:      "#c8d8f0",
          }}
        >
          <span style={{ color: "#00e676", flexShrink: 0, marginTop: 1 }}>—</span>
          <span>{renderInline(line.replace(/^[—\-]\s*/, ""))}</span>
        </div>
      )
      continue
    }

    // Regular paragraph line
    elements.push(
      <div
        key={`p-${i}`}
        style={{ fontSize: 13, lineHeight: 1.7, color: "#c8d8f0", marginBottom: 1 }}
      >
        {renderInline(line)}
      </div>
    )
  }

  if (inTable) {
    elements.push(renderTable(tableRows, "end"))
  }

  return <div>{elements}</div>
}
