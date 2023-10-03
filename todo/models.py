from django.db import models

# 투두 모델 정의
# 제목, 내용, 날짜기한 설정, 작성한날짜, 완료표시,
# 새로운 필드 추가해보기; 우선순위 낮음,중간,높음 선택하기 (choice필드)


class Todo(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=[
        ('낮음', '낮음'),
        ('중간', '중간'),
        ('높음', '높음'),
    ], default='중간')
    # choices 필드 사용햐서 우선순위 옵션을 정해주기

    def __str__(self):
        return self.title
