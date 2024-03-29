const http = require('http')
const serverApp = require('./server')
const { readFileSync } = require("fs");
const { init, startLoop } = require('./function');


const jsonPath = '../boxyz_json.json'
var json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
let port = json.settings.server.port
let host = json.settings.server.host


setTimeout(() => {
    init()
}, 1000)

serverApp.set('port', port);
const server = http.createServer(serverApp);

server.listen(port, host, () => {

    console.log(`Server is running on http://${host}:${port}`)
    setInterval(() => {
        startLoop()
    }, 2000
    )
})