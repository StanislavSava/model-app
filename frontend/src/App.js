import { useState, useRef, useEffect } from "react";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Scroll to bottom on new message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!prompt.trim()) return;
    setLoading(true);

    try {
      const res = await fetch("http://model:80/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      setMessages([...messages, { user: prompt, bot: data.response }]);
      setPrompt("");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-auto h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white shadow-xl rounded-xl flex flex-col overflow-hidden">
        {/* Chat Window */}
        <div className="chat-box flex-1 p-6 space-y-4 overflow-y-auto h-96">
          {messages.length === 0 && (
            <p className="text-gray-400 text-center">
              Start chatting with the assistant...
            </p>
          )}
          {messages.map((m, i) => (
            <div key={i} className="flex flex-col space-y-1">
              <div className="self-start bg-blue-100 text-blue-800 px-5 py-3 rounded-xl max-w-md">
                <span className="font-semibold">You:</span> {m.user}
              </div>
              <div className="self-end bg-green-100 text-green-800 px-5 py-3 rounded-xl max-w-md">
                <span className="font-semibold">Bot:</span> {m.bot}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* Input */}
        <div className="p-6 border-t flex space-x-3 bg-gray-50">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-6 py-4 border rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg"
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button
            onClick={sendMessage}
            className="bg-blue-600 text-white px-8 py-4 rounded-2xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg font-semibold shadow-md"
            disabled={loading}
          >
            {loading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}