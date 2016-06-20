#!/usr/bin/env node

var sys = require('sys')
var exec = require('child_process').exec;

exec("python /home/sjg/windVane/LEDStrip.py -x off", puts);
party(); 

setInterval(function() {
	party(); 
}, 3 * 1000);

var lastVal = 0; 

function party(){
	var rand = Math.floor(Math.random() * 32);
	var val = Math.round((rand / 32) * 100);
	console.log(rand + ":" + val);
	exec("python /home/sjg/windVane/LEDStrip.py -x percentageSmooth " + lastVal + " " + val, puts);
	lastVal = val;
}

function puts(error, stdout, stderr) { i=0; }


