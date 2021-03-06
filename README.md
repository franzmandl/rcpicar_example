# RCPiCar: Radio-controlled Raspberry Pi Car - Example

## Usage

### Set up as client

1. Install GStreamer 1.0. How to do this depends on your operating system. Using ArchLinux you just need to run `sudo pacman -S gstreamer gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good gst-plugins-ugly`.
2. Install the project and its dependencies by running `pip3 install .[client]`.
3. Run `rcpicar_client_gtk`.

### Set up as server

1. Enable the camera and I2C interface of the Raspberry Pi by running `sudo raspi-config`.
2. Install GStreamer 1.0 by running `sudo apt-get install gstreamer1.0-tools`.
3. Enable pigpio by running `sudo systemctl enable --now pigpiod`.
4. Install the project and its dependencies by running `pip3 install .[server]`.
5. Run `rcpicar_server`.

## Development

1. Create a venv directory by running `./make.py venv` and do not forget to activate it before the next step.
2. Install the project and its dependencies by running `pip3 install --editable .[tests]`.
3. Run the static type checker and style checker by running `./make.py check`.

## Links

[Here](https://github.com/franzmandl/rcpicar) is the library used by this project.
