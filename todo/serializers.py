from rest_framework import serializers
from .models import Todo


# 1)전체 리스트 조회용 - TodoListSerializer
# 2)특정 투두 조회용 - TodoDetailSerializer
# 3)생성용 - TodoCreateSerializer

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:  # 모델 클래스 내부 클래스로 모델의 동작과 메타데이터 설정할때 사용
        model = Todo
        fields = ('id', 'title', 'complete', 'priority', 'due_date')


class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description',
                  'complete', 'priority', 'due_date')


class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'priority', 'due_date')
