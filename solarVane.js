#!/usr/bin/env node

// Set LED Strip based on current weather forecast from client.raw

var http = require('http');
var httpLightServer = require('http');

var csv = require('csv');

var sys = require('sys')
var exec = require('child_process').exec;

var bulbID = 6;
//var wetherHost = "www.casa.ucl.ac.uk";
//var clientRawLocation = "/weather/clientraw.txt";

var wetherHost = "weather.casa.ucl.ac.uk";
var clientRawLocation = "/realtime.txt";

var previousValue = "";

var lastVal = 0;

var options = {
  host: wetherHost,
  port: 80,
  path: clientRawLocation
};

var max = 100.0;

exec("python /home/sjg/windVane/LEDStrip.py -x off", puts);
getWeather(); 

setInterval(function() {
	getWeather(); 
}, 3 * 1000);

function getWeather(){
	http.get(options, function(res) {

	  	res.on('data', function (dataClient) {
				  	if(res.statusCode == 200){
						parseRealtime(dataClient);
					}
	

		});
	
	}).on('error', function(e) {
	  console.log("Got error: " + e.message);
	});
}

function parseClientRaw(dataClient){
						var arr = dataClient.toString().split(" ");
						var val = parseFloat(arr[34]);
						var per = Math.round(val / max.toFixed(1) * 100);
					 	console.log("Solar: " + val + "\t\tMAX: " + max + "\t\tLCD: " + per + "%");
						exec("python /home/sjg/windVane/LEDStrip.py -x gradient " + per + " " + per, puts);
						lastVal = per;
}

function parseRealtime(dataClient){
						var arr = dataClient.toString().split(" ");
						var val = parseFloat(arr[56]);
						var solar = parseFloat(arr[45]);
						var per = Math.round(solar / val.toFixed(1) * 100);
					 	console.log("Solar: " + val + "\t\tMAX: " + max + "\t\tLCD: " + per + "%");
						exec("python /home/sjg/windVane/LEDStrip.py -x gradient " + per + " " + per, puts);
						lastVal = per;
}

function puts(error, stdout, stderr) { i=0; }


