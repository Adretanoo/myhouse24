from django.db import models


class Images(models.Model):
    image = models.ImageField(upload_to="images/")


class Seo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.TextField()

    class Meta:
        db_table = "seo"


class MainPage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slide1 = models.ImageField(upload_to="slides1/", null=True, blank=True)
    slide2 = models.ImageField(upload_to="slides2/", null=True, blank=True)
    slide3 = models.ImageField(upload_to="slides3/", null=True, blank=True)
    is_url_application = models.BooleanField(default=True)
    seo = models.OneToOneField(Seo, on_delete=models.CASCADE)

    class Meta:
        db_table = "main_page"


class MainPageBlock(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    main_image = models.ImageField(upload_to="main_page/", null=True, blank=True)
    main_page = models.ForeignKey(MainPage, on_delete=models.CASCADE)

    class Meta:
        db_table = "main_page_block"


class AboutUsPage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    additional_title = models.CharField(max_length=200)
    additional_description = models.TextField()
    seo = models.OneToOneField(Seo, on_delete=models.CASCADE)

    class Meta:
        db_table = "about_us_page"


class AboutUsPageGallery(models.Model):
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    about_us_page = models.ForeignKey(AboutUsPage, on_delete=models.CASCADE)

    class Meta:
        db_table = "about_us_gallery"


class AboutUsPageAdditionalGallery(models.Model):
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    about_us_page = models.ForeignKey(AboutUsPage, on_delete=models.CASCADE)

    class Meta:
        db_table = "about_us_gallery_additional"


class AboutUsPageDocuments(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="about_files/")
    about_us_page = models.ForeignKey(AboutUsPage, on_delete=models.CASCADE)

    class Meta:
        db_table = "about_us_page_documents"


class ServicePage(models.Model):
    seo = models.ForeignKey(Seo, on_delete=models.CASCADE)

    class Meta:
        db_table = "service_page"


class ServiceCard(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    main_image = models.ImageField(upload_to="service_card/", null=True, blank=True)
    service_page = models.ForeignKey(ServicePage, on_delete=models.CASCADE)

    class Meta:
        db_table = "service_card"


class TariffsPage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    seo = models.OneToOneField(Seo, on_delete=models.CASCADE)

    class Meta:
        db_table = "tariffs_page"


class TariffsCard(models.Model):
    signature = models.CharField(max_length=200)
    main_image = models.ImageField(upload_to="tariffs_card/", null=True, blank=True)
    tariffs_page = models.ForeignKey(TariffsPage, on_delete=models.CASCADE)

    class Meta:
        db_table = "tariffs_card"


class ContactsPage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link_site = models.URLField()
    map = models.TextField()
    fio = models.CharField(max_length=200)
    location = models.TextField(max_length=200)
    address = models.TextField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    seo = models.OneToOneField(Seo, on_delete=models.CASCADE)

    class Meta:
        db_table = "contacts_page"
