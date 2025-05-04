import { connect } from 'livekit-client';
import WebSocket from 'ws';
import fetch from 'node-fetch';

// CONFIGURATION
const LIVEKIT_WS_URL = 'wss://YOUR_DOMAIN.livekit.cloud'; // Replace with your LiveKit URL
const TOKEN_SERVER_URL = 'http://localhost:3000/token';   // Your token server
const PYTHON_WS_URL = 'ws://localhost:8765';              // Python WebSocket server
const ROOM_NAME = 'test-room';
const IDENTITY = 'subscriber-client';

async function fetchToken(identity, room) {
  const res = await fetch(`${TOKEN_SERVER_URL}?identity=${identity}&room=${room}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch token: ${await res.text()}`);
  }
  return res.text();
}

(async () => {
  const token = await fetchToken(IDENTITY, ROOM_NAME);

  const room = await connect(LIVEKIT_WS_URL, token, {
    autoSubscribe: true,
  });

  console.log(`✅ Connected to LiveKit room: ${ROOM_NAME}`);

  const pySocket = new WebSocket(PYTHON_WS_URL);

  pySocket.on('open', () => {
    console.log('🔗 Connected to Python WebSocket');

    room.on('trackSubscribed', (track, publication, participant) => {
      if (track.kind === 'audio') {
        console.log(`🎤 Subscribed to ${participant.identity}'s audio track`);

        // Listen to raw audio data and forward to Python
        track.onData = (data) => {
          if (pySocket.readyState === WebSocket.OPEN) {
            pySocket.send(data);
          }
        };
      }
    });
  });

  pySocket.on('error', (err) => {
    console.error('WebSocket error:', err);
  });

})();
