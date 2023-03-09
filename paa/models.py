from django.db import models


class KeyWordOfPaa(models.Model):
    keyword = models.CharField(max_length=100)
    numoftimes = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.id}, {self.keyword}"


class KeyWordAnswer(models.Model):
    keywordofpaa = models.ForeignKey(KeyWordOfPaa, related_name='result', on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        data = {'question': self.question, 'answer': self.answer}
        return f"{data}"


class KeyWordRelated(models.Model):
    keywordofpaa = models.ForeignKey(KeyWordOfPaa, related_name='related_search', on_delete=models.CASCADE)
    related_search = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.related_search


class KeyWordImages(models.Model):
    keywordofpaa = models.ForeignKey(KeyWordOfPaa, related_name='images', on_delete=models.CASCADE)
    image = models.TextField()

    def __str__(self):
        return f"{self.image}"


class KeyWordVideos(models.Model):
    keywordofpaa = models.ForeignKey(KeyWordOfPaa, related_name='youtube_videos', on_delete=models.CASCADE)
    video = models.TextField()

    def __str__(self):
        return f"{self.video}"


class KeyWordGoogleImages(models.Model):
    keywordofpaa = models.ForeignKey(KeyWordOfPaa, related_name='google_images', on_delete=models.CASCADE)
    image = models.TextField(null=True)

    def __str__(self):
        return f"{self.image}"

