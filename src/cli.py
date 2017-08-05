import io
import time

import click
import serial
from PIL import Image

version = "0.0.1"
usb_port = "/dev/ttyUSB0"
baud_rate = 57600


class NejeImage:
    def __init__(self, file_path):
        try:
            im = Image.open(file_path)
        except FileNotFoundError as e:
            click.secho('{}: {}'.format(e.strerror, e.filename), fg='red')
            exit()
        else:
            im = im.resize((512, 512), Image.NEAREST)
            im = im.convert('1').transpose(Image.FLIP_TOP_BOTTOM)

            self.image = im

            _bytes = io.BytesIO()
            im.save(_bytes, format='BMP')
            self.data = _bytes.getvalue()

    def view(self):
        self.image.show()

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
            click.secho('nejemojo is go', fg='green')
        else:
            click.secho('bad mojo: {}'.format(res), fg='red')

    def read(self):
        while True:
            # click.secho(str(self.ser.read(1), 'utf8', 'ignore'), fg='yellow', nl=False)
            # click.secho(str(self.ser.read(1), 'ascii', 'ignore'), fg='yellow', nl=False)
            print(self.ser.read(1))

    def engrave_memory(self):
        self.ser.write(b'\x40')
        # engrave
        self.ser.write(b'\xF1')

    def engrave_pause(self):
        self.ser.write(b'\xF2')

    def engrave_preview(self):
        self.ser.write(b'\xF4')

    def reset(self):
        self.ser.write(b'\xF9')

    def move_home(self):
        click.secho('Moving home...')
        self.ser.write(b'\xF3')
        time.sleep(5)

    def move_center(self):
        self.ser.write(b'\xFB')

    def move_up(self, distance=1):
        [self.ser.write(b'\xF5\x01') for _ in range(0, distance)]

    def move_down(self, distance=1):
        [self.ser.write(b'\xF5\x02') for _ in range(0, distance)]

    def move_left(self, distance=1):
        [self.ser.write(b'\xF5\x03') for _ in range(0, distance)]

    def move_right(self, distance=1):
        [self.ser.write(b'\xF5\x04') for _ in range(0, distance)]

    def erase(self):
        """ erase eeprom """

        click.secho('Erasing EEPROM:', nl=False, fg='yellow')

        for i in range(8):
            click.secho(str(i), nl=False)
            self.ser.write(b'\xFE')

        click.secho('\ndone')

    def load_image(self, image_data):
        self.erase()
        time.sleep(3)
        click.secho('writing image data to EEPROM')
        self.ser.write(image_data)
        click.secho('done uploading, press button to burn')


class Config:
    pass


@click.group()
@click.option('-p', '--port', default=usb_port, help='The serial port', show_default=True)
@click.pass_context
def cli(ctx, port):
    neje = Neje(port=port)
    ctx.obj.neje = neje


@cli.command('view')
@click.argument('name')
def view(name):
    """ View the image"""

    NejeImage(name).view()


@cli.command('load')
@click.argument('name')
@click.pass_context
def load(ctx, name):
    """ Load the image"""

    neje = ctx.obj.neje
    image_data = NejeImage(name).get()
    neje.load_image(image_data=image_data)
    neje.move_home()


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


@cli.command('box')
@click.pass_context
def box(ctx):
    """ Draws preview box"""
    ctx.obj.neje.engrave_preview()


@cli.command('reset')
@click.pass_context
def reset(ctx):
    """Reset Neje"""
    ctx.obj.neje.reset()


def neje():
    cli(obj=Config())


@click.command()
@click.argument('name')
def view(name):
    """ View the image"""

    NejeImage(name).view()
