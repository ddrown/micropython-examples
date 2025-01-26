#!/bin/sh

if [ -L /dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_013EFFA0-if00-port0 ]; then
  export AMPY_PORT=/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_013EFFA0-if00-port0
elif [ -L /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 ]; then
  export AMPY_PORT=/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0
else
  echo serial port not found
  exit 1
fi
~/esp32/ampy/bin/ampy "$@"
