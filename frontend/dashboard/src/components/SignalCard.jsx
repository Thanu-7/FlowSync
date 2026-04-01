function SignalCard({ title, status }) {
  return (
    <div style={{
      border: "2px solid black",
      padding: "20px",
      width: "200px",
      textAlign: "center",
      borderRadius: "10px"
    }}>
      <h2>{title}</h2>
      <h1 style={{
        color: status === "GREEN" ? "green" : "red"
      }}>
        {status}
      </h1>
    </div>
  );
}

export default SignalCard;