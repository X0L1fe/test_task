from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
    
class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name= 'items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True, null=True)
    named_url = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey('self',blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        if self.named_url:
            return f'/{self.named_url}/'
        elif self.url:
            return self.url
        else:
            return '#'