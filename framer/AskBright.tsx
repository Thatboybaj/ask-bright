// Ask Bright — floating chat widget for Framer
// Paste into a new Framer code file, then drag it onto your page.
import { useState, useRef, useEffect } from "react"
import { addPropertyControls, ControlType } from "framer"

type Source = { title: string; url: string }
type Msg = { role: "user" | "bot"; text: string; sources?: Source[] }

export default function AskBright(props) {
    const { apiUrl, title, subtitle, accent, suggestions } = props
    const [open, setOpen] = useState(false)
    const [msgs, setMsgs] = useState<Msg[]>([])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)
    const [sessionId, setSessionId] = useState<string | null>(null)
    const logRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        logRef.current?.scrollTo(0, logRef.current.scrollHeight)
    }, [msgs, loading])

    async function ask(question: string) {
        if (!question.trim() || loading) return
        setMsgs((m) => [...m, { role: "user", text: question }])
        setInput("")
        setLoading(true)
        try {
            const res = await fetch(`${apiUrl.replace(/\/$/, "")}/api/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: question, session_id: sessionId }),
            })
            const data = await res.json()
            if (!res.ok) throw new Error(data.detail || "Request failed")
            setSessionId(data.session_id)
            setMsgs((m) => [...m, { role: "bot", text: data.answer, sources: data.sources }])
        } catch (e) {
            setMsgs((m) => [...m, { role: "bot", text: "Sorry, something went wrong. Please try again." }])
        } finally {
            setLoading(false)
        }
    }

    const font = "Inter, system-ui, sans-serif"

    return (
        <div style={{ position: "fixed", right: 24, bottom: 24, zIndex: 9999, fontFamily: font }}>
            {open && (
                <div style={{
                    position: "absolute", right: 0, bottom: 72,
                    width: "min(380px, calc(100vw - 32px))", height: "min(560px, calc(100vh - 120px))",
                    background: "#fff", color: "#141414", borderRadius: 16,
                    boxShadow: "0 12px 40px rgba(0,0,0,0.18)", border: "1px solid #e4e2dc",
                    display: "flex", flexDirection: "column", overflow: "hidden",
                }}>
                    <div style={{ padding: "16px 18px", borderBottom: "1px solid #e4e2dc" }}>
                        <div style={{ fontWeight: 600, fontSize: 15 }}>{title}</div>
                        <div style={{ fontSize: 13, color: "#6b6b6b" }}>{subtitle}</div>
                    </div>

                    <div ref={logRef} style={{ flex: 1, overflowY: "auto", padding: 16, display: "flex", flexDirection: "column", gap: 10 }}>
                        {msgs.length === 0 && (
                            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                                {suggestions.map((s: string) => (
                                    <button key={s} onClick={() => ask(s)} style={{
                                        border: "1px solid #e4e2dc", background: "none", borderRadius: 999,
                                        padding: "6px 12px", fontSize: 13, cursor: "pointer", fontFamily: font, color: "#141414",
                                    }}>{s}</button>
                                ))}
                            </div>
                        )}
                        {msgs.map((m, i) => (
                            <div key={i} style={{
                                alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                                maxWidth: "85%", padding: "10px 13px", borderRadius: 14, fontSize: 14, lineHeight: 1.5,
                                whiteSpace: "pre-wrap",
                                background: m.role === "user" ? accent : "transparent",
                                color: m.role === "user" ? "#fff" : "#141414",
                                border: m.role === "user" ? "none" : "1px solid #e4e2dc",
                            }}>
                                {m.text}
                                {m.sources && m.sources.length > 0 && (
                                    <div style={{ marginTop: 8, fontSize: 12, color: "#6b6b6b" }}>
                                        Sources:{" "}
                                        {m.sources.map((s, j) => (
                                            <span key={s.title}>
                                                <a href={s.url || "#"} target="_blank" rel="noreferrer" style={{ color: "inherit" }}>{s.title}</a>
                                                {j < m.sources!.length - 1 ? " · " : ""}
                                            </span>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                        {loading && <div style={{ fontSize: 13, color: "#6b6b6b", fontStyle: "italic" }}>Thinking…</div>}
                    </div>

                    <form onSubmit={(e) => { e.preventDefault(); ask(input) }}
                        style={{ display: "flex", gap: 8, padding: 12, borderTop: "1px solid #e4e2dc" }}>
                        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type a question…"
                            style={{ flex: 1, padding: "10px 12px", border: "1px solid #e4e2dc", borderRadius: 10, fontSize: 14, fontFamily: font, outline: "none" }} />
                        <button type="submit" disabled={loading} style={{
                            padding: "10px 14px", border: 0, borderRadius: 10, background: accent, color: "#fff",
                            fontSize: 14, cursor: "pointer", fontFamily: font, opacity: loading ? 0.6 : 1,
                        }}>Send</button>
                    </form>
                </div>
            )}

            <button onClick={() => setOpen(!open)} aria-label="Open chat" style={{
                width: 56, height: 56, borderRadius: "50%", border: 0, background: accent, color: "#fff",
                fontSize: 22, cursor: "pointer", boxShadow: "0 6px 20px rgba(0,0,0,0.2)",
            }}>{open ? "×" : "✦"}</button>
        </div>
    )
}

AskBright.defaultProps = {
    apiUrl: "https://ask-bright.vercel.app",
    title: "Ask Bright",
    subtitle: "Ask about my projects, skills and services.",
    accent: "#141414",
    suggestions: [
        "What Framer work has Bright done?",
        "Does he build custom code components?",
        "What certifications does he have?",
    ],
}

addPropertyControls(AskBright, {
    apiUrl: { type: ControlType.String, title: "API URL" },
    title: { type: ControlType.String, title: "Title" },
    subtitle: { type: ControlType.String, title: "Subtitle" },
    accent: { type: ControlType.Color, title: "Accent" },
    suggestions: { type: ControlType.Array, title: "Suggestions", control: { type: ControlType.String } },
})
