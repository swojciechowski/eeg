import os, sys
print(sys.executable)

import usb

REQUEST_TYPE_SEND = usb.util.build_request_type(
    usb.util.CTRL_OUT,
    usb.util.CTRL_TYPE_CLASS,
    usb.util.CTRL_RECIPIENT_DEVICE
)

REQUEST_TYPE_RECEIVE = usb.util.build_request_type(
    usb.util.CTRL_IN,
    usb.util.CTRL_TYPE_CLASS,
    usb.util.CTRL_RECIPIENT_DEVICE
)

USBRQ_HID_GET_REPORT = 0x01
USBRQ_HID_SET_REPORT = 0x09
USB_HID_REPORT_TYPE_FEATURE = 0x03

def getStringDescriptor(device, index):
    response = device.ctrl_transfer(
        usb.util.ENDPOINT_IN,
        usb.legacy.REQ_GET_DESCRIPTOR,
        (usb.util.DESC_TYPE_STRING << 8) | index,
        0,
        255
    )

    # TODO: Refer to 'libusb_get_string_descriptor_ascii' for error handling

    return response[2:].tostring().decode('utf-16')


class DigiUSB:
    def __init__(self, idVendor, idProduct):
        self.idVendor = idVendor
        self.idProduct = idProduct

        self.device = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
        if not self.device:
            raise ValueError("Device not found")

    def write(self, byte):
        self._transfer(REQUEST_TYPE_SEND, USBRQ_HID_SET_REPORT, byte, [])

    def read(self):
        response = self._transfer(REQUEST_TYPE_RECEIVE, USBRQ_HID_GET_REPORT, 0, 1)

        return bytes(response)

    def _transfer(self, request_type, request, index, value):
        return self.device.ctrl_transfer(
            request_type, request,
            (USB_HID_REPORT_TYPE_FEATURE << 8) | 0,
            index,
            value,
        )

    @property
    def productName(self):
        return getStringDescriptor(self.device, self.device.iProduct)

    @property
    def manufacturer(self):
        return getStringDescriptor(self.device, self.device.iManufacturer)
