import { useEffect, useState } from "react";
import SignalCard from "./SignalCard";

function Dashboard() {
  const [data, setData] = useState({
    road_A: "RED",
    road_B: "RED",
    timer: 0,
    emergency: false,
    count_A: 0,
    count_B: 0
  });

  const fetchData = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/traffic/dual");
      const result = await res.json();
      console.log("DATA:", result);
      setData(result);
    } catch (err) {
      console.log("Error fetching data");
    }
  };

  useEffect(() => {
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ textAlign: "center" }}>

      {/* SIGNALS */}
      <div style={{ display: "flex", justifyContent: "space-around", marginTop: "40px" }}>
        <SignalCard title="Road A" status={data.road_A} />
        <SignalCard title="Road B" status={data.road_B} />
      </div>

      {/* TIMER */}
      <h2>⏱ Timer: {data.timer}s</h2>

      {/* VEHICLE COUNTS */}
      <p>🚗 Road A: {data.count_A}</p>
      <p>🚗 Road B: {data.count_B}</p>

      {/* 🚑 EMERGENCY STATUS */}
      {data.emergency && (
        <h2 style={{ color: "red", marginTop: "20px" }}>
          🚑 EMERGENCY ACTIVE - ALL SIGNALS GREEN
        </h2>
      )}

      {/* BUTTONS */}
      <div style={{ marginTop: "30px" }}>
        <button
          onClick={() =>
            fetch("http://127.0.0.1:8000/traffic/emergency", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ road: "A" })
            })
          }
          style={{
            padding: "10px",
            backgroundColor: "red",
            color: "white",
            marginRight: "10px"
          }}
        >
          🚑 Emergency A
        </button>

        <button
          onClick={() =>
            fetch("http://127.0.0.1:8000/traffic/clear", {
              method: "POST"
            })
          }
          style={{
            padding: "10px",
            backgroundColor: "gray",
            color: "white"
          }}
        >
          ❌ Clear
        </button>
      </div>
    </div>
  );
}

export default Dashboard;