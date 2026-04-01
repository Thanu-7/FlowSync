import { useEffect, useState } from "react";
import SignalCard from "./SignalCard";

function Dashboard() {
  const [data, setData] = useState({
    road_A: "RED",
    road_B: "RED",
    timer: 0
  });

  const fetchData = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/traffic/dual");
      const result = await res.json();
      setData({...result});
    } catch (err) {
      console.log("Error fetching data");
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000); // refresh every 2 sec
    return () => clearInterval(interval);
  }, []);

return (
  <div style={{ textAlign: "center" }}>

    {/* 🚦 SIGNAL DISPLAY */}
    <div style={{display: "flex", justifyContent: "space-around", marginTop: "40px"}}>
      <SignalCard title="Road A" status={data.road_A} />
      <SignalCard title="Road B" status={data.road_B} />
    </div>

    {/* ⏱ TIMER */}
    <h2 style={{marginTop: "20px"}}>⏱ Timer: {data.timer}s</h2>

    {/* 🎥 VIDEO SECTION */}
    <div style={{display: "flex", justifyContent: "center", gap: "20px", marginTop: "30px"}}>
      <video src="/road1.mp4" width="300" autoPlay loop muted />
      <video src="/road2.mp4" width="300" autoPlay loop muted />
    </div>

    {/* 🚑 EMERGENCY BUTTON */}
    <div style={{marginTop: "30px"}}>
      <button 
        onClick={() => fetch("http://127.0.0.1:8000/traffic/emergency", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ road: "A" })
        })}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: "red",
          color: "white",
          border: "none",
          borderRadius: "8px"
        }}
      >
        🚑 Emergency Road A
      </button>
    </div>

  </div>
);
}

export default Dashboard;