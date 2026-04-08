# FinWise — AI Assistant Frontend Integration
### Antigravity IDE Prompt

---

## Context

You are integrating a pre-built, modular AI Assistant feature into the existing FinWise React frontend. The `AIAssistant/` folder has already been dropped into the project directory. Your job is **purely UI wiring** — routing, navigation, layout fit, CSS import, and the page shell component. Do not touch any business logic, context providers, API services, or existing pages.

---

## Project Structure (existing, do not modify)

```
FRNTD/
├── src/
│   ├── App.jsx                        ← Add route here
│   ├── main.jsx
│   ├── layouts/
│   │   └── DashboardLayout.jsx
│   ├── components/
│   │   └── Sidebar.jsx                ← Add nav link here
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   └── FinanceContext.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── NetWorth.jsx
│   │   ├── BudgetPlanner.jsx
│   │   ├── Expenses.jsx
│   │   ├── Loans.jsx
│   │   ├── Insights.jsx
│   │   └── Settings.jsx
│   ├── services/
│   │   └── api.js
│   └── styles/
│       └── global.css
├── AIAssistant/                       ← dropped in, do not restructure
│   ├── components/
│   │   ├── index.js
│   │   ├── AssistantSidebar.jsx
│   │   ├── ChatInput.jsx
│   │   ├── ConversationView.jsx
│   │   ├── EmptyState.jsx
│   │   ├── MarkdownRenderer.jsx
│   │   ├── MessageBubble.jsx
│   │   ├── SessionRow.jsx
│   │   └── ThinkingIndicator.jsx
│   ├── constants/
│   │   ├── index.js
│   │   ├── featureCards.js
│   │   └── mockData.js
│   ├── hooks/
│   │   ├── index.js
│   │   ├── useAssistantChat.js
│   │   └── useTypewriter.js
│   ├── utils/
│   │   └── index.js
│   └── styles/
│       └── assistant.css
└── package.json
```

---

## Task 1 — Create the Page Shell

Create a new file at:

```
FRNTD/src/pages/AIAssistant.jsx
```

This file is the page shell. It wires the hook to the UI components. It does not contain any business logic, context calls, or API calls of its own.

Write the file with exactly this content:

```jsx
import { useState, useRef, useEffect } from "react"
import { ChevronRight, RotateCcw } from "lucide-react"
import { useAssistantChat }  from "../../AIAssistant/hooks"
import {
  AssistantSidebar,
  EmptyState,
  ConversationView,
  ChatInput,
} from "../../AIAssistant/components"
import "../../AIAssistant/styles/assistant.css"

export default function AIAssistantPage() {
  const {
    sessions, activeId, messages, thinking, latestAI, isEmpty,
    send, newChat, loadSession, deleteSession,
  } = useAssistantChat()

  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [input,       setInput]       = useState("")
  const bottomRef = useRef(null)
  const inputRef  = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, thinking])

  function handleSend(content, triggeredBy = null) {
    if (!content.trim()) return
    send(content, triggeredBy)
    setInput("")
  }

  return (
    <div className="fw-root">
      {/* Sidebar */}
      <AssistantSidebar
        sessions={sessions}
        activeId={activeId}
        isOpen={sidebarOpen}
        onNewChat={newChat}
        onLoadSession={loadSession}
        onDeleteSession={deleteSession}
      />

      {/* Main column */}
      <div className="fw-main">
        <div className="fw-noise" />

        {/* Header */}
        <div className="fw-header">
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <button
              className="fw-toggle"
              onClick={() => setSidebarOpen(o => !o)}
            >
              <ChevronRight
                size={15}
                style={{
                  transform: sidebarOpen ? "rotate(180deg)" : "rotate(0deg)",
                  transition: "transform 0.22s",
                }}
              />
            </button>
            <div>
              <div style={{
                fontSize: 10, fontWeight: 500, letterSpacing: "0.1em",
                textTransform: "uppercase", color: "#3a5070", marginBottom: 3,
              }}>
                AI-powered analysis
              </div>
              <h1 style={{
                fontFamily: "'Syne', sans-serif", fontSize: 22,
                fontWeight: 700, letterSpacing: "-0.015em",
                lineHeight: 1, color: "#f0f4ff",
              }}>
                Assistant
              </h1>
            </div>
          </div>

          {!isEmpty && (
            <button className="fw-newchat-sm" onClick={newChat}>
              <RotateCcw size={12} /> New Chat
            </button>
          )}
        </div>

        {/* Messages */}
        <div className="fw-messages">
          {isEmpty ? (
            <EmptyState onSend={handleSend} isThinking={thinking} />
          ) : (
            <ConversationView
              messages={messages}
              thinking={thinking}
              latestAI={latestAI}
              onSend={handleSend}
              bottomRef={bottomRef}
            />
          )}
          {isEmpty && <div ref={bottomRef} />}
        </div>

        {/* Input */}
        <ChatInput
          value={input}
          onChange={setInput}
          onSend={handleSend}
          isThinking={thinking}
          inputRef={inputRef}
        />
      </div>
    </div>
  )
}
```

---

## Task 2 — Register the Route in App.jsx

Open `FRNTD/src/App.jsx`.

**Step 1 — Add the import** at the top of the file, alongside the other page imports:

```jsx
import AIAssistantPage from "./pages/AIAssistant"
```

**Step 2 — Add the route** inside the existing protected `<Route>` block that wraps `<DashboardLayout />`. Add it as a sibling to the other page routes:

```jsx
<Route path="/assistant" element={<AIAssistantPage />} />
```

The full block after your edit should look like this (existing routes unchanged, new one added at the end):

```jsx
<Route element={
  <ProtectedRoute>
    {needsOnboarding ? <Navigate to="/onboarding" replace /> : <DashboardLayout />}
  </ProtectedRoute>
}>
  <Route path="/"           element={<Dashboard />}        />
  <Route path="/net-worth"  element={<NetWorth />}         />
  <Route path="/budget"     element={<BudgetPlanner />}    />
  <Route path="/expenses"   element={<Expenses />}         />
  <Route path="/loans"      element={<Loans />}            />
  <Route path="/insights"   element={<Insights />}         />
  <Route path="/settings"   element={<Settings />}         />
  <Route path="/assistant"  element={<AIAssistantPage />}  />  {/* ← ADD THIS */}
</Route>
```

Do not modify any other part of App.jsx.

---

## Task 3 — Add the Navigation Link in Sidebar.jsx

Open `FRNTD/src/components/Sidebar.jsx`.

**Step 1 — Add the Sparkles icon** to the existing lucide-react import at the top of the file. The current import line is:

```jsx
import {
  LayoutDashboard, TrendingUp, Calculator,
  Receipt, CreditCard, Lightbulb, Settings, LogOut, User
} from "lucide-react"
```

Change it to:

```jsx
import {
  LayoutDashboard, TrendingUp, Calculator,
  Receipt, CreditCard, Lightbulb, Settings, LogOut, User, Sparkles
} from "lucide-react"
```

**Step 2 — Add the nav entry** to the existing `NAV` array. The current array is:

```jsx
const NAV = [
  { to: "/",          icon: LayoutDashboard, label: "Dashboard"      },
  { to: "/net-worth", icon: TrendingUp,      label: "Net Worth"      },
  { to: "/budget",    icon: Calculator,      label: "Budget Planner" },
  { to: "/expenses",  icon: Receipt,         label: "Expenses"       },
  { to: "/loans",     icon: CreditCard,      label: "Loans"          },
  { to: "/insights",  icon: Lightbulb,       label: "Insights"       },
]
```

Add the new entry at the bottom of the array:

```jsx
const NAV = [
  { to: "/",           icon: LayoutDashboard, label: "Dashboard"      },
  { to: "/net-worth",  icon: TrendingUp,      label: "Net Worth"      },
  { to: "/budget",     icon: Calculator,      label: "Budget Planner" },
  { to: "/expenses",   icon: Receipt,         label: "Expenses"       },
  { to: "/loans",      icon: CreditCard,      label: "Loans"          },
  { to: "/insights",   icon: Lightbulb,       label: "Insights"       },
  { to: "/assistant",  icon: Sparkles,        label: "AI Assistant"   },  // ← ADD THIS
]
```

Do not modify any other part of Sidebar.jsx.

---

## Task 4 — Verify the CSS Import Does Not Conflict

Open `FRNTD/src/styles/global.css` and confirm that it does **not** already contain any class names beginning with `.fw-`. If it does, flag it — do not auto-resolve.

The `AIAssistant/styles/assistant.css` file uses a `.fw-` prefix on every class name specifically to avoid collisions with the app's global styles. No edits to `global.css` are needed.

---

## Task 5 — Verify the Layout Renders Correctly

The `AIAssistantPage` component renders inside `DashboardLayout`, which wraps every page with `<Sidebar />` on the left and `<main className="content">` on the right.

The `.fw-root` class sets `height: 100%` and `display: flex`. For it to fill the available space correctly, the parent `<main className="content">` must have a definite height. 

Open `FRNTD/src/styles/global.css` and find the `.content` rule:

```css
.content {
  flex: 1;
  padding: 32px 36px;
  overflow-y: auto;
  background: var(--bg-base);
}
```

The AI Assistant page needs its own padding handling (the internal layout manages its own spacing). Add a targeted override **after** the existing `.content` rule — do not modify the existing rule itself:

```css
/* AI Assistant page — override content padding so the internal layout fills edge-to-edge */
.content:has(.fw-root) {
  padding: 0;
  overflow: hidden;
}
```

This selector only fires when `.content` contains `.fw-root`, so no other page is affected.

---

## What NOT to Do

- Do not move, rename, or restructure anything inside `AIAssistant/`
- Do not import or call `useFinance()` or `useAuth()` in any of the new files
- Do not add any API calls
- Do not modify any existing page components (`Dashboard.jsx`, `Insights.jsx`, etc.)
- Do not modify `main.jsx`, `AuthContext.jsx`, `FinanceContext.jsx`, or `api.js`
- Do not install any new npm packages — all dependencies (`lucide-react`, `react`, `react-router-dom`) are already present in `package.json`
- Do not change the `AIAssistant/` folder location — import paths in the page shell are written relative to `src/pages/`, resolving to `../../AIAssistant/`

---

## Expected Result

After completing all four tasks, the application should:

1. Show an **"AI Assistant"** entry in the left sidebar nav, with a `Sparkles` icon, sitting below "Insights"
2. Navigate to `/assistant` when clicked
3. Render the full AI Assistant interface — sidebar with session history, empty state with feature cards, chat input — inside the existing dashboard shell
4. All existing pages and routes remain completely unaffected
5. The dev server (`npm run dev`) starts without errors or warnings related to these changes

---

## Import Path Reference

| File being edited | Import path to AIAssistant module |
|---|---|
| `src/pages/AIAssistant.jsx` | `../../AIAssistant/hooks` |
| `src/pages/AIAssistant.jsx` | `../../AIAssistant/components` |
| `src/pages/AIAssistant.jsx` | `../../AIAssistant/styles/assistant.css` |

These paths assume `AIAssistant/` lives at the project root alongside `src/`. If it is placed inside `src/` instead, update all `../../AIAssistant/` prefixes to `../AIAssistant/`.

---

## File Edit Summary

| File | Action | Scope |
|---|---|---|
| `src/pages/AIAssistant.jsx` | **Create** | New file, full content provided above |
| `src/App.jsx` | **Edit** | Add 1 import line + 1 route line |
| `src/components/Sidebar.jsx` | **Edit** | Add `Sparkles` to import + 1 nav entry |
| `src/styles/global.css` | **Edit** | Add 4-line CSS override after `.content` rule |
| Everything inside `AIAssistant/` | **No touch** | Read-only |
| All other existing files | **No touch** | Read-only |
