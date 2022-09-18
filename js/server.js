const express = require('express')
const { up, down, init, getJson } = require('./function');


const serverApp = express()

serverApp.get('/', (req, res) => {
    res.status(200).send('ON');
})


//Get information
serverApp.get('/get/json/all', (req, res) => {
    res.status(200).json(getJson());
})

serverApp.get('/get/json/clock', (req, res) => {
    res.status(200).json(getJson().clock);
})

serverApp.get('/get/json/thermostas', (req, res) => {
    res.status(200).json(getJson().thermostas);
})

serverApp.get('/get/temprature', (req, res) => {
    res.status(200).send(getJson().thermostas.temperature);
})

serverApp.get('/get/state', (req, res) => {
    res.status(200).send(getJson().thermostas.state);
})

//Set information

serverApp.get('/set/temperature', (req, res) => {
    res.status(200).json(getJson().thermostas);
})

serverApp.get('/set/state', (req, res) => {
    res.status(200).json(getJson().thermostas.temperature);
})

serverApp.get('/set/thermosUp', (req, res) => {
    res.status(200).send("increase")
    up()
})

serverApp.get('/set/thermosDown', (req, res) => {
    res.status(200).send("decrease")
    down()
})

serverApp.get('/init', (req, res) => {
    res.status(200).send('Initilised')
    init()
})

module.exports = serverApp;
