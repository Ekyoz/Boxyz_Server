let http = require('http')
const { readFileSync, writeFileSync } = require("fs");

const jsonPath = 'boxyz_json.json'
var json = JSON.parse(readFileSync(jsonPath, 'utf-8'));

let port = json.settings.server.port
let host = json.settings.server.host


const server = http.createServer(function (req, res) {
    json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    switch (req.url) {
        case "/":
            res.writeHead(200, { "Content-Type": "text/html" });
            res.end("ON");
            break


        //Get information

        case "/get/json/all":
            res.writeHead(200, { "Content-Type": "application/json" });
            res.end(JSON.stringify(json));
            break

        case "/get/json/clock":
            res.writeHead(200, { "Content-Type": "application/json" });
            res.end(JSON.stringify(json.clock));
            break

        case "/get/json/thermostas":
            res.writeHead(200, { "Content-Type": "application/json" });
            res.end(JSON.stringify(json.thermostas));
            break

        case "/get/temprature":
            res.writeHead(200, { "Content-Type": "text/html" });
            res.end(JSON.stringify(json.thermostas.temperature));
            break

        case "/get/state":
            res.writeHead(200, { "Content-Type": "text/html" });
            res.end(JSON.stringify(json.thermostas.state));
            break


        //Set information

        case "/set/temprature":
            json.thermostas.temperature = 


        case "/set/state":

        case "/set/thermosUp":
            res.writeHead(200, { "Content-Type": "text/html" });
            res.end("increase");
            Up()
            break

        case "/set/thermosDown":
            res.writeHead(200, { "Content-Type": "text/html" });
            res.end("decrease");
            Down()
            break


        default:
            res.writeHead(404);
            res.end("error")
            break
    }
}).listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});


function Up() {
    temp = json.thermostas.temperature
    tempMax = json.settings.tempMax
    if (temp < tempMax) {
        json.thermostas.temperature = json.thermostas.temperature + 1
        writeFileSync(jsonPath, JSON.stringify(json, null, 6))
    }
    SetTemporalyOn()
    console.log("The temperature has increased by 1 and the status is true")
}

function Down() {
    temp = json.thermostas.temperature
    tempMin = json.settings.tempMin
    if (tempMin < temp) {
        json.thermostas.temperature = json.thermostas.temperature - 1
        writeFileSync(jsonPath, JSON.stringify(json, null, 6))
    }
    SetTemporalyOn()
    console.log("The temperature has decreased by 1 and the status is true")
}

function SetTemporalyOn() {
    const currentTime = new Date()
    const endTime = new Date()

    endTime.setHours(parseInt(currentTime.getHours()) + parseInt(json.settings.clockTimeToDefaultHour))
    endTime.setMinutes(parseInt(currentTime.getMinutes()) + parseInt(json.settings.clockTimeToDefaultMin))

    if ((json.thermostas.Temporarily == false) & (json.thermostas.TemporarilyStart == null) & (json.thermostas.TemporarilyEnd == null)) {
        json.thermostas.Temporarily = true
        json.thermostas.TemporarilyStart = `${("0" + currentTime.getHours()).slice(-2)}:${("0" + currentTime.getMinutes()).slice(-2)}`
        json.thermostas.TemporarilyEnd = `${("0" + endTime.getHours()).slice(-2)}:${("0" + endTime.getMinutes()).slice(-2)}`
        writeFileSync(jsonPath, JSON.stringify(json, null, 6))
    }
}

function SetTemporalyOff() {
    json.thermostas.Temporarily = false
    json.thermostas.TemporarilyStart = null
    json.thermostas.TemporarilyEnd = null
    writeFileSync(jsonPath, JSON.stringify(json, null, 6))
}

