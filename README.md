# USB-HID-parser

### Usage keystroke.py
```
$ python keystroke.py <file capture.txt>
```
### Extract file capture.txt from pcap 
```
$ tshark -r <file pcap> -T fields -e usbhid.data -Y "(usbhid.data or usb.capdata) and usb.data_len eq 8" > capture.txt
```
If the output don't have ':' between each bytes please use this command:
```
$ tshark -r <file pcap> -T fields -e usbhid.data -Y "(usbhid.data or usb.capdata) and usb.data_len eq 8" | sed 's/../:&/g2' > capture.txt
```

### Usage parser.py
```
$ python parser.py
```
Need file usbhid.data.hex as input.

### Extract file usbhid.data.hex from pcap 
```
$ tshark -r <file pcap> -T fields -u s -e _ws.col.Time -e usbhid.data -Y usbhid.data > usbhid.data.hex 
```