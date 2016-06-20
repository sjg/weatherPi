#!/usr/bin/env node

// Set Phillips Hue Bulb based on current weather forecast from client.raw

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

var options = {
  host: wetherHost,
  port: 80,
  path: clientRawLocation
};

var max = 27.8072; // 32MPH

exec("python /home/sjg/windVane/LEDStrip.py -x off", puts);
getWeather(); 

setInterval(function() {
	getWeather(); 
}, 2 * 1000);

function getWeather(){
	http.get(options, function(res) {

	  	res.on('data', function (dataClient) {
				  	if(res.statusCode == 200){
					    	var arr = dataClient.toString().split(" ");
					    	var avg = parseInt(arr[1]);
					    	var gusts = parseFloat(arr[2]);
					    	var maxWind = parseInt(arr[071]);
						var val = gusts;
						
						var per = Math.round((kntToMPH(val) / kntToMPH(max)) * 100);

						if(lastVal != per){
					 		console.log("GUST: " + kntToMPH(val) + "\t\tMAX: " + kntToMPH(max) + "\t\tLCD: " + per + "%");
							exec("python /home/sjg/windVane/LEDStrip.py -x percentage " + lastVal + " " + per, puts);
						}

						lastVal = per;
					}
	

		});
	
	}).on('error', function(e) {
	  console.log("Got error: " + e.message);
	});
}

function kntToMPH(knottVal){
	return 1.15077945 * knottVal;
}

function puts(error, stdout, stderr) { sys.puts(stdout) }


