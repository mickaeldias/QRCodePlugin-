from cms.models import CMSPlugin, Page
from django.utils.translation import gettext_lazy as _
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


LINK_CHOICES = (
    ("https://www.google.com/", "https://www.google.com/"),
    ("https://github.com/", "https://github.com/")
)


class QRCodeModel(CMSPlugin):
    qr_code = models.ImageField(
        editable=False,
        upload_to='qr_code'
    )
    qr_code_link = models.URLField(
        editable=False,
        null=True
    )
    end_date = models.DateTimeField(
        editable=False,
        null=True
    )


    class Meta:
        abstract = True



class QRCodePlugin(QRCodeModel):
    internal_link = models.ForeignKey(
        Page,
        verbose_name=_('Internal Link'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        help_text=_('If provided, overrides the external link.')
    )
    external_link = models.URLField(
        verbose_name=_('External Link'),
        null=True,
        blank=True,
        choices=LINK_CHOICES
    )
    name = models.CharField(
        max_length=60
    )
    start_date = models.DateTimeField(
        auto_now_add=True
    )
    activate = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


    def save(self, *args, **kwargs):
        try:
            self.qr_code_link = self.internal_link.get_absolute_url()
        except:
            self.qr_code_link = self.external_link


        qrcode_img = qrcode.make(self.qr_code_link)
        fname = f"qr_code-{self.name}.png"

        buffer = BytesIO()
        qrcode_img.save(buffer, format="PNG")
        self.qr_code.save(fname, File(buffer), save=False)


        if self.activate == False:
            self.end_date = self.updated_at
        else:
            self.end_date = None


        super(QRCodePlugin, self).save(*args, **kwargs)
        
