import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { TypeAnimation } from "react-type-animation";
import { Send, Stethoscope } from "lucide-react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setReply("");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();

      // IMPORTANT: store FULL reply only
      setReply(data.reply || "");
    } catch {
      setReply("Backend not responding.");
    }

    setMessage("");
    setLoading(false);
  };

  return (
    <div className="app-container">
    <div className="header">
  <Stethoscope size={32} className="logo" />
  <h1 className="title">Doctor's Assistant</h1>
</div>

    

   
      <div className="chat-box">
        {loading && <p className="loading">Thinking...</p>}

        {!loading && reply && (
          <div className="assistant-message">
            <TypeAnimation
              sequence={[reply]}
              speed={120}
              cursor={false}
              wrapper="div"
            >
              {(text) => <ReactMarkdown>{text}</ReactMarkdown>}
            </TypeAnimation>
          </div>
        )}
      </div>

      <div className="input-wrapper">
        <textarea
  className="input-box"
  placeholder="Enter clinical question..."
  value={message}
  onChange={(e) => setMessage(e.target.value)}
  onKeyDown={(e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();   // stop newline
      sendMessage();        // send message
    }
  }}
/>
<Send className="send-icon" onClick={sendMessage} />

      </div>
    </div>
  );
}

export default App;
