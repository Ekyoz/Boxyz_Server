const { readFileSync, writeFileSync } = require("fs");
const http = require('http');


const jsonPath = '../boxyz_json.json'


//---USEFUL FUNCTION FOR APP-----//

function up() { //Augmente de 1 la temperature
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    temp = json.thermostas.temperature
    tempMax = json.settings.thermostas.temperature.tempMax
    if (temp < tempMax) {
        json.thermostas.temperature = json.thermostas.temperature + 1
        writeFileSync(jsonPath, JSON.stringify(json, null, 6))
    }
    setTemporalyOn()
}

function down() { //Diminue de 1 la temperature
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    temp = json.thermostas.temperature
    tempMin = json.settings.thermostas.temperature.tempMin
    if (tempMin < temp) {
        json.thermostas.temperature = json.thermostas.temperature - 1
        writeFileSync(jsonPath, JSON.stringify(json, null, 6))
    }
    setTemporalyOn()
}

function setOn(temperature) {
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    const IP = json.settings.thermostas.ip
    const PORT = json.settings.thermostas.port
    const URL = `http://${IP}:${PORT}/heat?heater=1&heat=${temperature}`
    http.get(URL, (resp) => {
        setState(true)
    }).on("error", (err) => {
        setState(false)
    });
}

function setOff() {
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    const IP = json.settings.thermostas.ip
    const PORT = json.settings.thermostas.port
    const URL = `http://${IP}:${PORT}/heat?heater=0&heat=${json.thermostas.temperature}`
    http.get(URL, (resp) => {
        setState(false)
    }).on("error", (err) => {
        setState(false)
    });
    setTemp(json.settings.thermostas.temperature.tempDefault)
}

function setTemporalyOn() { //Active le mode temporaire et mets les plage horraire actuelle
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    const currentTime = new Date()
    const endTime = new Date()

    endTime.setHours(parseInt(currentTime.getHours()) + parseInt(json.settings.temporary.clockTimeToDefaultHour))
    endTime.setMinutes(parseInt(currentTime.getMinutes()) + parseInt(json.settings.temporary.clockTimeToDefaultMin))

    if ((json.thermostas.temporary.state == false) & (json.thermostas.temporary.temporaryStart == null) & (json.thermostas.temporary.temporaryEnd == null)) {
        json.thermostas.temporary.state = true
        json.thermostas.temporary.temporaryStart = `${("0" + currentTime.getHours()).slice(-2)}:${("0" + currentTime.getMinutes()).slice(-2)}`
        json.thermostas.temporary.temporaryEnd = `${("0" + endTime.getHours()).slice(-2)}:${("0" + endTime.getMinutes()).slice(-2)}`
        writeFileSync(jsonPath, JSON.stringify(json, null, 6))
    }
}

function setTemporalyOff() { //Desctive le mode temporaire
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    json.thermostas.temporary.state = false
    json.thermostas.temporary.temporaryStart = null
    json.thermostas.temporary.temporaryEnd = null
    writeFileSync(jsonPath, JSON.stringify(json, null, 6))
}

function setState(state) {
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    json.thermostas.state = state
    writeFileSync(jsonPath, JSON.stringify(json, null, 6))
}

function setTemp(temperature) {
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    json.thermostas.temperature = temperature
    writeFileSync(jsonPath, JSON.stringify(json, null, 6))
}



//----FUNCTION FOR SERVER----//

function startLoop() {
    json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    if (checkPower() == true) {
        checkTimeSlot()
        checkTemporaly()
    }
    if (checkPower() == false) {
        setOff()
        setTemporalyOff()
    }
}

function init() { //Remet toute les variable a zero
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    setTemp(json.settings.thermostas.tempDefault)
    json.system.current_on = null
    json.thermostas.state = false
    json.thermostas.temporary.state = false
    json.thermostas.temporary.temporaryStart = null
    json.thermostas.temporary.temporaryEnd = null
    writeFileSync(jsonPath, JSON.stringify(json, null, 6))
    const IP = json.settings.thermostas.ip
    const PORT = json.settings.thermostas.port
    const TEMP_DEFAULT = json.settings.thermostas.tempDefault
    const URL = `http://${IP}:${PORT}/init?state=${json.thermostas.state}&heat=${TEMP_DEFAULT}`

    function checkInitialised() {
        if ((json.system.current_on == null) && (!json.thermostas.state) && (!json.thermostas.temporary.state) && (json.thermostas.temporary.temporaryStart == null) && (json.thermostas.temporary.temporaryEnd == null)) {
            console.log("System initialised")
        }
        if (!((json.system.current_on == null) && (!json.thermostas.state) && (!json.thermostas.temporary.state) && (json.thermostas.temporary.temporaryStart == null) && (json.thermostas.temporary.temporaryEnd == null))) {
            console.log("System not initialised")
            process.exit()
        }
        http.get(URL, (resp) => {
            if (resp.statusCode == 200) {
                console.log("Thermostas initialised")
            }
        }).on("error", (err) => {
            console.error("Thermostas not initialised")
        });
    }
    checkInitialised()
}

function checkTimeSlot() { //Met la plage horraire actuellement active dans le json ou le met a null
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'))
    var daysList = new Array()
    for (let index = -1; index < Object.keys(json.days).length; index++) {
        const element = Object.keys(json.days)[index];
        daysList.push(element)
    }

    const currentTime = new Date()
    const actualDay = daysList[currentTime.getDay() || 7]

    for (let index = 0; index < json.days[actualDay].length; index++) {
        const actualStartClockTimeSlot = new Date()
        actualStartClockTimeSlot.setHours(parseInt(JSON.stringify(json.clock.timeSlot[json.days[actualDay][index]].hourStart).split(':')[0].replace('"', '')))
        actualStartClockTimeSlot.setMinutes(parseInt(JSON.stringify(json.clock.timeSlot[json.days[actualDay][index]].hourStart).split(':')[1].replace('"', '')))

        const actualEndClockTimeSlot = new Date()
        actualEndClockTimeSlot.setHours(parseInt(JSON.stringify(json.clock.timeSlot[json.days[actualDay][index]].hourEnd).split(':')[0].replace('"', '')))
        actualEndClockTimeSlot.setMinutes(parseInt(JSON.stringify(json.clock.timeSlot[json.days[actualDay][index]].hourEnd).split(':')[1].replace('"', '')))

        if (json.thermostas.temporary.state == false) {
            if (json.clock.timeSlot[json.days[actualDay][index]].state == true) {
                if ((currentTime.getTime() >= actualStartClockTimeSlot.getTime()) && (currentTime.getTime() <= actualEndClockTimeSlot.getTime())) {
                    json.system.current_on = json.days[actualDay][index]
                    json.thermostas.temperature = json.clock.timeSlot[json.days[actualDay][index]].temp
                    writeFileSync(jsonPath, JSON.stringify(json, null, 6))
                    const temperature = json.clock.timeSlot[json.system.current_on].temp
                    setOn(temperature)
                    setTemp(temperature)
                }
                else {
                    json.system.current_on = null
                    writeFileSync(jsonPath, JSON.stringify(json, null, 6))
                    setOff()
                    setTemp(json.settings.thermostas.temperature.tempDefault)
                }
            }
            else {
                json.system.current_on = null
                writeFileSync(jsonPath, JSON.stringify(json, null, 6))
                setTemp(json.settings.thermostas.temperature.tempDefault)
                setOff()
            }
        }
        if (json.thermostas.temporary.state == true) {
            json.system.current_on = null
            writeFileSync(jsonPath, JSON.stringify(json, null, 6))
            setTemporalyOn()
        }
    }
}

function checkTemporaly() { //Check lorsque le mode temporaly est activer et set on / off le thermsotas
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'))
    const currentTime = new Date()

    if (json.thermostas.temporary.state == true) {
        const actualStartClockTemporary = new Date()
        actualStartClockTemporary.setHours(parseInt(JSON.stringify(json.thermostas.temporary.temporaryStart).split(':')[0].replace('"', '')))
        actualStartClockTemporary.setMinutes(parseInt(JSON.stringify(json.thermostas.temporary.temporaryStart).split(':')[1].replace('"', '')))

        const actualEndClockTemporary = new Date()
        actualEndClockTemporary.setHours(parseInt(JSON.stringify(json.thermostas.temporary.temporaryEnd).split(':')[0].replace('"', '')))
        actualEndClockTemporary.setMinutes(parseInt(JSON.stringify(json.thermostas.temporary.temporaryEnd).split(':')[1].replace('"', '')))

        if ((currentTime.getTime() >= actualStartClockTemporary.getTime()) && (currentTime.getTime() <= actualEndClockTemporary.getTime())) {
            const temperature = json.thermostas.temperature // recupere la temperature de la plage horraire actuelle
            setOn(temperature)
            setTemp(temperature)
        }
        else {
            setTemporalyOff()
            setOff()
        }
    }
    if (json.thermostas.temporary.state == false) {
        setTemporalyOff()
        if (json.system.current_on == false) {
            setOff()
        }
    }
}

function getJson() {
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    return json
}

function checkPower() {
    const json = JSON.parse(readFileSync(jsonPath, 'utf-8'));
    if (json.system.power == true) {
        return true
    }
    if (json.system.power == false) {
        json.system.current_on = null
        json.thermostas.state = false
        json.thermostas.temporary.state = false
        json.thermostas.temporary.temporaryStart = null
        json.thermostas.temporary.temporaryEnd = null
        writeFileSync(jsonPath, JSON.stringify(json, null, 6))
        return false
    }
}

module.exports = {
    up,
    down,
    setOn,
    setOff,
    setTemporalyOn,
    setTemporalyOff,
    setState,
    setTemp,
    init,
    checkTemporaly,
    checkTimeSlot,
    getJson,
    checkPower,
    startLoop
}