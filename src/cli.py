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

        self.data = im.tobitmap()

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
        self.ser.write(b'\xF3')

    def move_center(self):
        self.ser.write(b'\xFB')

    def load_image(self, image_data):
        a = 0
        while a < 8:
            a = a + 1
            print('Erase EEPROM 8/' + str(a))
            # erase eeprom
            self.ser.write(b'\xFE')

        # upload to eeprom
        self.ser.write(image_data)


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
    ctx.obj.neje.load_image(image_data=NejeImage(name).get())


@cli.command('burn')
@click.pass_context
def burn(ctx):
    ctx.obj.neje.engrave_memory()


@cli.command('pause')
@click.pass_context
def pause(ctx):
    ctx.obj.neje.engrave_pause()


@cli.command('home')
@click.pass_context
def home(ctx):
    ctx.obj.neje.move_home()


@cli.command('preview')
@click.pass_context
def preview(ctx):
    ctx.obj.neje.engrave_preview()


@cli.command('reset')
@click.pass_context
def reset(ctx):
    ctx.obj.neje.reset()


if __name__ == '__main__':
    cli(obj=Config())
