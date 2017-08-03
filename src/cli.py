import serial
import click

version = "0.0.1"
usb_port = "/dev/ttyUSB0"
baud_rate = 57600


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

    def send_image(self, image_data):
        a = 0
        while a < 8:
            a = a + 1
            print('Erase EEPROM 8/' + str(a))
            # erase eeprom
            self.ser.write(b'\xFE')

        # upload to eeprom
        self.ser.write(image_data)


@click.group()
@click.option('-p', '--port', default=usb_port, help='The serial port', show_default=True)
def cli(port):
    neje = Neje(port=port)
    neje.engrave_memory()
    # neje.move_center()
    # neje.engrave_preview()

@cli.command('preview')
def preview():
    ctx

