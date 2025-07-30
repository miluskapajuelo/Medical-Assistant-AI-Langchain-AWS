
import React, { useState } from 'react';
import { Box, Container, Paper, Avatar, Typography, TextField, IconButton, Stack } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

function App() {

  const [msgs, setMsgs] = React.useState([])
  const [text, setText] = React.useState("")


const sendMessage = async (e) => {
  e.preventDefault();

  const now = new Date();
  const time = now.getHours() + ':' + now.getMinutes().toString().padStart(2, '0');

  const userMsg = {
    text, from:"human", time
  }

  setMsgs(m=> [...m, userMsg])
  setText("")

  // call the backend API to get the response
  const res = await fetch(
    '/api',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        msg: userMsg.text,
      })
    }
  )

  const systemText = await res.text();
  const systemmsg = {
    text: systemText, from:"system", time
  }
  setMsgs(m=> [...m, systemmsg])
}

  return (
    <Box sx={{ height: '100vh', bgcolor: 'background.default', p: 2 }}>
      <Container maxWidth="sm" sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Paper elevation={3} sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
          {/* Header */}
          <Box sx={{ p: 2, display: 'flex', alignItems: 'center', borderBottom: 1, borderColor: 'divider' }}>
            <Avatar src="https://cdn-icons-png.flaticon.com/512/387/387569.png" />
            <Typography variant="h6" sx={{ ml: 2 }}>Medical Chatbot</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>Ask me anything!</Typography>
          </Box>

          {/* Messages */}
          <Box sx={{ flexGrow: 1, p: 2, overflowY: 'auto' }}>
            {msgs.map((m, i) => (
              <Stack
                key={i}
                direction="row"
                spacing={1}
                justifyContent={m.from === 'user' ? 'flex-end' : 'flex-start'}
                sx={{ mb: 2 }}
              >
                {m.from === 'bot' && <Avatar src="https://cdn-icons-png.flaticon.com/512/387/387569.png" sx={{ width: 32, height: 32 }} />}
                <Paper
                  sx={{ p: 1.5, maxWidth: '70%', bgcolor: m.from === 'user' ? 'primary.light' : 'grey.200' }}
                >
                  <Typography variant="body1">{m.text}</Typography>
                  <Typography variant="caption" display="block" align={m.from === 'user' ? 'right' : 'left'}>
                    {m.time}
                  </Typography>
                </Paper>
                {m.from === 'user' && <Avatar src="https://i.ibb.co/d5b84Xw/Untitled-design.png" sx={{ width: 32, height: 32 }} />}
              </Stack>
            ))}
          </Box>

          {/* Input */}
          <Box component="form" onSubmit={sendMessage} sx={{ p: 1, borderTop: 1, borderColor: 'divider', display: 'flex' }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Type your message..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <IconButton type="submit" color="primary" sx={{ ml: 1 }}>
              <SendIcon />
            </IconButton>
          </Box>
        </Paper>
      </Container>
    </Box>
  );


}

export default App;
