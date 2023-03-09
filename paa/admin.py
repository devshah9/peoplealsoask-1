from django.contrib import admin

from .models import KeyWordAnswer, KeyWordOfPaa, KeyWordRelated, KeyWordImages, KeyWordVideos, KeyWordGoogleImages


# Register your models here.


@admin.register(KeyWordOfPaa)
class KeyWordOfPaaAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword', 'numoftimes')


@admin.register(KeyWordAnswer)
class KeyWordAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'keywordofpaa', 'question', 'answer')


@admin.register(KeyWordRelated)
class KeyWordRelatedAdmin(admin.ModelAdmin):
    list_display = ('id', 'keywordofpaa', 'related_search')


@admin.register(KeyWordImages)
class KeyWordImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'keywordofpaa', 'image')


@admin.register(KeyWordVideos)
class KeyWordVideosAdmin(admin.ModelAdmin):
    list_display = ('id', 'keywordofpaa', 'video')


@admin.register(KeyWordGoogleImages)
class KeyWordGoogleImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'keywordofpaa', 'image')
