import time

import click
import serial
from PIL import Image

version = "0.0.1"
usb_port = "/dev/ttyUSB0"
baud_rate = 57600


class NejeImage:
    def __init__(self, file_path):
        im = Image.open(file_path)

        im = im.resize((512, 512), Image.NEAREST)
        im = im.convert('1').transpose(Image.FLIP_TOP_BOTTOM)

        self.data = im.getdata()

    def get(self):
        return self.data


class Neje:
    """ A neje machine """

    def __init__(self, port):
        self.ser = serial.Serial(
            port=port,
            baudrate=baud_rate,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        self.ser.write(b'\xF6')
        res = self.ser.read(2)
        if res == b'e\xfb':
            print('nejemojo is go')
        else:
            print('no mojo: {}'.format(res))

    def read(self):
        while True:
            print(self.ser.read(1))

    def engrave_memory(self):
        # set 60 ms
        self.ser.write(b'\x3C')
        # engrave
        self.ser.write(b'\xF1')

    def engrave_pause(self):
        self.ser.write(b'\xF2')

    def engrave_preview(self):
        self.ser.write(b'\xF4')

    def reset(self):
        self.ser.write(b'\xF9')

    def move_home(self):
        print('Moving home...')
        self.ser.write(b'\xF3')
        time.sleep(5)

    def move_center(self):
        self.ser.write(b'\xFB')

    def erase(self):
        """ erase eeprom """

        print('Erasing EEPROM:', end='')

        for i in range(8):
            print(str(i), end='')
            self.ser.write(b'\xFE')

        print('\ndone')

    def load_image(self, image_data):
        self.erase()

        print('writing image data to EEPROM')
        self.ser.write(image_data)
        print('done uploading, press button to burn')


class Config:
    pass


@click.group()
@click.option('-p', '--port', default=usb_port, help='The serial port', show_default=True)
@click.pass_context
def cli(ctx, port):
    neje = Neje(port=port)
    ctx.obj.neje = neje


@cli.command('load')
@click.argument('name')
@click.pass_context
def load(ctx, name):
    """ Load the image"""
    image_data = NejeImage(name).get()
    ctx.obj.neje.load_image(image_data=image_data)


@cli.command('burn')
@click.pass_context
def burn(ctx):
    """ Burn the image """
    ctx.obj.neje.engrave_memory()

@cli.command('read')
@click.pass_context
def burn(ctx):
    """ Read from port"""
    ctx.obj.neje.read()

@cli.command('erase')
@click.pass_context
def burn(ctx):
    """ Erase image from eeprom"""
    ctx.obj.neje.erase()


@cli.command('pause')
@click.pass_context
def pause(ctx):
    """ Pause Neje burning"""
    ctx.obj.neje.engrave_pause()


@cli.command('home')
@click.pass_context
def home(ctx):
    """ Move to home position """
    ctx.obj.neje.move_home()


@cli.command('preview')
@click.pass_context
def preview(ctx):
    """ Draws preview box"""
    ctx.obj.neje.engrave_preview()


@cli.command('reset')
@click.pass_context
def reset(ctx):
    """Reset Neje"""
    ctx.obj.neje.reset()


def main():
    cli(obj=Config())
