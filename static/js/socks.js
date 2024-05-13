const WebSocket = require('ws');
const ws = new WebSocket('ws://127.0.0.1:9043');

ws.onopen = () => {
    console.log('connection ok')

    let data = {
        "from": "user1",
        "to": "user2",
        "content": "ооо",
        "chat_id": "1"
    };

    ws.send(JSON.stringify(data));
}


ws.onerror = (error) => {
    console.log(error)
}