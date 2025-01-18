const express = require("express");
const { Server } = require("socket.io");
const http = require("http");
const { PythonShell } = require("python-shell");
const path = require("path");

const app = express();
const server = http.createServer(app);
// const io = new Server(server);

// Add CORS headers
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  if (req.method === "OPTIONS") {
    return res.sendStatus(200);
  }
  next();
});

// Serve static files (e.g., front-end for uploading audio)
app.use(express.static("public"));

// Endpoint for uploading audio files
app.post("/upload", (req, res) => {
  console.log("Received upload request");

  const audioPath = path.join(__dirname, "harvard.wav");
  // Optional: reference text for WER calculation
  const referenceText = `The stale smell of old beer lingers. It takes heat to bring out the odor. A cold dip restores health and zest. A salt pickle tastes fine with ham. Tacos al pastor are my favorite. A zestful food is the hot cross bun.`; // Your reference text

  const pythonOptions = {
    mode: "json", // Changed to json mode
    pythonPath: "python",
    scriptPath: path.join(__dirname, "scripts"),
    args: [audioPath, referenceText],
    pythonOptions: ["-u"],
  };

  let pyshell = new PythonShell("transcribe.py", pythonOptions);

  pyshell.on("message", function (message) {
    console.log("Received results:", message);
    res.json(message);
  });

  pyshell.on("error", function (err) {
    console.error("Python error:", err);
    res.status(500).json({ error: err.message });
  });
});

// // WebSocket for real-time transcription
// io.on("connection", (socket) => {
//   console.log("A client connected");

//   socket.on("audio-stream", (chunk) => {
//     console.log("Received audio chunk", chunk);
//     // You can process live audio chunks here
//   });

//   socket.on("disconnect", () => {
//     console.log("Client disconnected");
//   });
// });

server.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
