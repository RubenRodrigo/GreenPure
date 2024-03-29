import uuid
from django.db import models
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from user.models import Account

# Create your models here.


def get_product_image_filepath(instance, filename):
    return f'device/qrcode/{instance.unique_id}/{filename}'


def get_default_product_image():
    return 'default/default-device.jpg'


class Device(models.Model):
    account_created_id = models.ForeignKey(
        Account, related_name="device_created", on_delete=models.SET_NULL, null=True, blank=True)
    owner_id = models.ForeignKey(
        Account, related_name="device_owner", on_delete=models.SET_NULL, null=True, blank=True)
    activation_date = models.DateTimeField(default=timezone.now)
    device = models.CharField(max_length=100, null=True, blank=True)
    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    qr_code = models.ImageField(
        upload_to=get_product_image_filepath, null=True, blank=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return str(self.unique_id)

    def save(self, *args, **kwargs):
        account = self.account_created_id
        if not account.is_staff:
            raise ValidationError(_(
                ('You dont have enough permissions. {}'.format(account.email))))

        if bool(self.qr_code) is False:
            qrcode_img = qrcode.make(str(self.unique_id))
            canvas = Image.new('RGB',
                               (qrcode_img.pixel_size, qrcode_img.pixel_size),
                               'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.unique_id}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()

        return super(Device, self).save(*args, **kwargs)

    @ property
    def quality_AVG(self):
        data_item = self.data.all()
        total = sum([item.quality for item in data_item])
        return total
