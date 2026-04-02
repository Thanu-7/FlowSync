function SignalCard({ title, status }) {
  const getColor = (light) => {
    if (status === light) return light.toLowerCase();
    return "#444"; // inactive light
  };

  return (
    <div style={{
      border: "2px solid black",
      padding: "20px",
      width: "200px",
      textAlign: "center",
      borderRadius: "10px"
    }}>
      <h2>{title}</h2>

      {/* Traffic Light */}
      <div style={{
        background: "#857979",
        padding: "15px",
        borderRadius: "20px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "10px",
        width: "80px",
        margin: "auto"
      }}>
        
        {/* Red Light */}
        <div style={{
          width: "40px",
          height: "40px",
          borderRadius: "50%",
          backgroundColor: getColor("RED")
        }} />

        {/* Yellow Light */}
        <div style={{
          width: "40px",
          height: "40px",
          borderRadius: "50%",
          backgroundColor: getColor("YELLOW")
        }} />

        {/* Green Light */}
        <div style={{
          width: "40px",
          height: "40px",
          borderRadius: "50%",
          backgroundColor: getColor("GREEN")
        }} />

      </div>

      <p style={{ marginTop: "10px", fontWeight: "bold" }}>
        {status}
      </p>
    </div>
  );
}

export default SignalCard;