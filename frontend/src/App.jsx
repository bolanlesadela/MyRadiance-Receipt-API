import { useState } from "react";
import axios from "axios";

const ACCENT = "#B48C6E";
const BG = "#F5F0EB";
const DARK = "#3D2B1F";
const MUTED = "#A08060";

export default function App() {
  const [customer, setCustomer] = useState("");
  const [items, setItems] = useState([{ name: "", qty: 1, price: "" }]);
  const [loading, setLoading] = useState(false);

  const total = items.reduce((sum, i) => sum + (i.qty * (parseFloat(i.price) || 0)), 0);

  const addItem = () => setItems([...items, { name: "", qty: 1, price: "" }]);

  const removeItem = (index) => {
    if (items.length === 1) return;
    setItems(items.filter((_, i) => i !== index));
  };

  const updateItem = (index, field, value) => {
    const updated = [...items];
    updated[index][field] = value;
    setItems(updated);
  };

  const generateReceipt = async () => {
    if (!customer.trim()) return alert("Please enter a customer name.");
    const validItems = items.filter(i => i.name && i.price);
    if (validItems.length === 0) return alert("Please add at least one item.");

    setLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/generate-receipt",
        { customer, items: validItems.map(i => ({ ...i, qty: parseInt(i.qty), price: parseFloat(i.price) })) },
        { responseType: "blob" }
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "myradiance-receipt.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert("Something went wrong. Make sure the API is running.");
    }
    setLoading(false);
  };

  return (
    <div style={{ minHeight: "100vh", background: BG, fontFamily: "'Jost', sans-serif" }}>

      {/* Top accent bar */}
      <div style={{ height: 3, background: ACCENT }} />

      {/* Header */}
      <div style={{ textAlign: "center", padding: "48px 24px 32px" }}>
        <h1 style={{
          fontFamily: "'Great Vibes', cursive",
          fontSize: 64,
          color: DARK,
          margin: 0,
          lineHeight: 1.1
        }}>
          MyRadiance
        </h1>
        <p style={{
          fontFamily: "'Cormorant Garamond', serif",
          fontStyle: "italic",
          fontSize: 15,
          color: MUTED,
          letterSpacing: 3,
          marginTop: 8,
          textTransform: "uppercase"
        }}>
          Glow different. Glow radiant.
        </p>
        <div style={{ width: 60, height: 1, background: ACCENT, margin: "24px auto 0" }} />
      </div>

      {/* Order Builder */}
      <div style={{ maxWidth: 680, margin: "0 auto", padding: "0 24px 80px" }}>

        {/* Section label */}
        <p style={{
          fontSize: 10,
          letterSpacing: 4,
          textTransform: "uppercase",
          color: MUTED,
          marginBottom: 32
        }}>
          New Order
        </p>

        {/* Customer name */}
        <div style={{ marginBottom: 40 }}>
          <label style={labelStyle}>Client Name</label>
          <input
            value={customer}
            onChange={e => setCustomer(e.target.value)}
            placeholder="Enter client name"
            style={inputStyle}
          />
        </div>

        {/* Divider */}
        <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 28 }}>
          <div style={{ flex: 1, height: 1, background: "#DDD5CC" }} />
          <span style={{ fontSize: 10, letterSpacing: 3, color: MUTED, textTransform: "uppercase" }}>Order Items</span>
          <div style={{ flex: 1, height: 1, background: "#DDD5CC" }} />
        </div>

        {/* Column headers */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 80px 120px 32px", gap: 12, marginBottom: 12 }}>
          {["Product", "Qty", "Price (NGN)", ""].map((h, i) => (
            <span key={i} style={{ fontSize: 9, letterSpacing: 3, textTransform: "uppercase", color: MUTED }}>{h}</span>
          ))}
        </div>

        {/* Item rows */}
        {items.map((item, index) => (
          <div key={index} style={{ display: "grid", gridTemplateColumns: "1fr 80px 120px 32px", gap: 12, marginBottom: 12 }}>
            <input
              value={item.name}
              onChange={e => updateItem(index, "name", e.target.value)}
              placeholder="Product name"
              style={inputStyle}
            />
            <input
              type="number"
              value={item.qty}
              onChange={e => updateItem(index, "qty", e.target.value)}
              min={1}
              style={{ ...inputStyle, textAlign: "center" }}
            />
            <input
              type="number"
              value={item.price}
              onChange={e => updateItem(index, "price", e.target.value)}
              placeholder="0.00"
              style={{ ...inputStyle, textAlign: "right" }}
            />
            <button
              onClick={() => removeItem(index)}
              style={{
                background: "none",
                border: "none",
                color: "#CCC",
                cursor: "pointer",
                fontSize: 18,
                padding: 0,
                lineHeight: 1,
                alignSelf: "center"
              }}
            >
              ×
            </button>
          </div>
        ))}

        {/* Add item */}
        <button onClick={addItem} style={{
          background: "none",
          border: `1px dashed ${ACCENT}`,
          color: ACCENT,
          fontSize: 11,
          letterSpacing: 3,
          textTransform: "uppercase",
          padding: "10px 20px",
          cursor: "pointer",
          marginTop: 8,
          width: "100%",
          fontFamily: "'Jost', sans-serif"
        }}>
          + Add Item
        </button>

        {/* Total */}
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          borderTop: `1px solid #DDD5CC`,
          marginTop: 32,
          paddingTop: 20
        }}>
          <span style={{ fontSize: 10, letterSpacing: 4, textTransform: "uppercase", color: MUTED }}>Total</span>
          <span style={{
            fontFamily: "'Cormorant Garamond', serif",
            fontSize: 28,
            color: DARK,
            fontWeight: 300
          }}>
            NGN {total.toLocaleString("en-NG", { minimumFractionDigits: 2 })}
          </span>
        </div>

        {/* Generate button */}
        <button
          onClick={generateReceipt}
          disabled={loading}
          style={{
            width: "100%",
            marginTop: 32,
            padding: "18px 0",
            background: loading ? MUTED : DARK,
            color: BG,
            border: "none",
            fontSize: 11,
            letterSpacing: 5,
            textTransform: "uppercase",
            cursor: loading ? "not-allowed" : "pointer",
            fontFamily: "'Jost', sans-serif",
            transition: "background 0.3s"
          }}
        >
          {loading ? "Generating..." : "Generate Receipt"}
        </button>

      </div>

      {/* Bottom accent bar */}
      <div style={{ height: 3, background: ACCENT }} />
    </div>
  );
}

const inputStyle = {
  width: "100%",
  background: "transparent",
  border: "none",
  borderBottom: "1px solid #C8B9A8",
  padding: "10px 0",
  fontSize: 14,
  color: "#3D2B1F",
  fontFamily: "'Jost', sans-serif",
  outline: "none",
  boxSizing: "border-box"
};

const labelStyle = {
  display: "block",
  fontSize: 9,
  letterSpacing: 4,
  textTransform: "uppercase",
  color: "#A08060",
  marginBottom: 10
};