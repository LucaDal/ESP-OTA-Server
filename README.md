# ESP8266 OTA Server
This projects is made specifically for the ESP8266 board, but could work for every ESP board, just change some **#include** line in Network.h.

## Library
This **custom-OTA-ESP-library** allow to get updates from your own hosted server:

### Setup
In case you want an HTTPS connection call this function:
```
begin(EEPROMsize,"youraddress","fingerprint","API_KEY");
```
+ **EEPROMsize** of your board.
+ **youraddress** without the protocol ('https://') part
+ **fingerprint** of your hosted server, for example: "A2:2B:4E:GE:A8:0E:AH:10:7E:A1:BB:B9:01:BB:24:M9:E4:FC:45:AA"
+ **API_KEY** your own API_key

If you don't have a fingerprint call this instead 
```
  begin(EEPROMsize,"http://youraddress","API_KEY");
```
Here in the address specify the http protocol

### Loop

to check regularly if an update is uploaded use:
```
  checkUpdates(seconds);
```
that check updates every tot seconds

## Server

I needs to write that part...
