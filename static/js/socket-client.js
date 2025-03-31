const socket = io("http://localhost:5000"); // Connect to WebSocket server

// Listen for game state updates
socket.on("game_state", (data) => {
    console.log("Game State Updated:", data);
});

// Join a room
socket.emit("join_room", { room_id: "1234", player_name: "Alice" });

// Leave a room
socket.emit("leave_room", { room_id: "1234" });

// Handle errors
socket.on("error", (data) => {
    console.error("Error:", data.message);
});
