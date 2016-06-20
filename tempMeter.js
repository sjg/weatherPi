#!/usr/bin/env node

// Set LED Strip based on current weather forecast from client.raw

var cumulus = require("cumulus");

var http = require('http');
var httpLightServer = require('http');

var csv = require('csv');

var sys = require('sys')
var exec = require('child_process').exec;

var bulbID = 6;
var wetherHost = "www.casa.ucl.ac.uk";
var clientRawLocation = "/weather/clientraw.txt";

var previousValue = "";

var lastVal = 0;

//var version = "clientraw";
var version = "realtime";

if(version == "clientraw"){
	var options = {
		host: wetherHost,
 		port: 80,
 		path: clientRawLocation
	};
}else{
	// Realtime.txt
	var options = {
		host: "weather.casa.ucl.ac.uk",
 		port: 80,
 		path: "/realtime.txt"
	};	
}


console.log("Connecting to: " + options.host + options.path);

var max = 32.0;

exec("python /home/sjg/windVane/LEDStrip.py -x off", puts);
getWeather(); 

setInterval(function() {
	getWeather(); 
}, 3 * 1000);

function getWeather(){
	http.get(options, function(res) {

	  	res.on('data', function (dataClient) {
				  	if(res.statusCode == 200){
					    	if(version == "clientraw"){
							var arr = dataClient.toString().split(" ");
							var val = parseFloat(arr[4]);
							var per = Math.round(val / max.toFixed(1) * 100);
					 		console.log("Temp: " + val + "\t\tMAX: " + max + "\t\tLCD: " + per + "%");
							exec("python /home/sjg/windVane/LEDStrip.py -x percentageTemp " + per + " " + per, puts);
							lastVal = per;
						}else{
							var realtime = cumulus.parseToJson(dataClient.toString());
							var per = Math.round(realtime.temp / max.toFixed(1) * 100);
					 		console.log("Temp: " + realtime.temp + "\t\tMAX: " + max + "\t\tLCD: " + per + "%");
							exec("python /home/sjg/windVane/LEDStrip.py -x percentageTemp " + per + " " + per, puts);
							lastVal = per;
						}
					}else{
						console.log(dataClient.toString());
					}
	

		});
	
	}).on('error', function(e) {
	  console.log("Got error: " + e.message);
	});
}

function puts(error, stdout, stderr) { i=0; }


