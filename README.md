# RCPiCar: Radio-controlled Raspberry Pi Car - Example

## Usage

### Set up as client

1. Install GStreamer 1.0. How to do this depends on your operating system. Using ArchLinux you just need to run `sudo pacman -S gstreamer gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good gst-plugins-ugly`.
2. Install the project and its dependencies by running `pip install .[client]`.
3. Run `rcpicar_client_gtk`.

### Set up as server

1. Enable the camera and I2C interface of the Raspberry Pi by running `sudo raspi-config`.
2. Install GStreamer 1.0 by running `sudo apt-get install gstreamer1.0-tools`.
3. Enable pigpio by running `sudo systemctl enable --now pigpiod`.
4. Install the project and its dependencies by running `pip install .[server]`.
5. Run `rcpicar_server`.

## Links

[Here](https://github.com/franzmandl/rcpicar) is the library used by this project.
