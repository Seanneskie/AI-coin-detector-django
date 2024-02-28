from django.db import models

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')


class CoinEntry(models.Model):
    image = models.ImageField(upload_to='coin_images/')
    class_names_with_scores = models.JSONField()

    def __str__(self):
        return f"CoinEntry {self.id}"

class CoinCounter(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"CoinCounter: {self.count}"