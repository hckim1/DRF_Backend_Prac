from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoListSerializer, TodoDetailSerializer, TodoCreateSerializer

# 1)전체 조회뷰 - TodoView
#   Get - 필터로 완료된 투두들만 todos 변수로 가져오기; (TodoListSerializer) status 200
#   Post - 작성하기; 작성한 투두(request.data)를 TodoCreateSerializer로 파싱하고 직렬,
#          유효검사하고 .save로 역직렬화하고 .data 저장 201 아니면 .errors 400때리기
# 2)특정 투두 조회뷰 - TodoDetailView
#   Get - 검색조건으로 id필드가 pk값과 일치하면 todo 변수에 넣고 아니면 404때리기; (TodoDetailSerializer)
#   Put - 수정하기; 1)Get처럼 먼저 검색조건으로 id=pk하고 2)수정한 투두(request.data)를 TodoCreateSerializer로 파싱하고 직렬,
#          3)유효검사하고 4).save로 역직렬화하고 5).data 저장 201 6)아니면 .errors 400때리기#
#   Delete - 삭제하기; 1)검색조건으로 id필드가 pk값과 일치하면 todo 변수에 넣고 아니면 404때리기; 2) .delete
# 3)완료된 전체 조회뷰 - TodoDoneView
#   Get - 완료된 투두들만 가져오기; (TodoListSerializer) status 200
# 4)완료된 특정 투두 조회뷰 - TodoDetailDoneView
#   Get -  필터로 완료되지 않은 투두들만 dones 변수로 가져오기;
#   Delete -삭제하기; 1)검색조건으로 id필드가 pk값과 일치하면 done 변수에 넣고 아니면 404때리기; 2) .delete


class TodoView(APIView):
    def get(self, request):
        todos = Todo.objects.filter(complete=False)  # 완료안된 투두 데이터를 가져오고
        serializer = TodoListSerializer(todos, many=True)  # 가져온 데이터를 직렬화한후
        # 직렬화된 serializer.data를 HTTP응답으로 200반환
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)  # 작성된 data를 직렬화한후
        if serializer.is_valid():  # 유효검사 진행(데이터 모델의 필드랑 일치하는지도 검사함)
            serializer.save()  # 통과되면 역직렬화(파이썬 객체로 변환시킨다음 데이터베이스에 저장)
            # 통과된 경우 직렬화된 data를 HTTP응답으로 201반환
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 통과하지 못한 경우 HTTP응답으로 400반환
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailView(APIView):
    def get(self, request, pk):
        # 투두 모델에서 특정 투두의 id가 pk와 같다면 todo 변수에 들어감 아니면 404떄리기
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoDetailSerializer(todo)  # 가져온 데이터를 직렬화 시키고
        # 직렬화된 serializer.data를 HTTP응답으로 200반환
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # 투두 모델에서 특정 투두의 id가 pk와 같다면 todo 변수에 들어감 아니면 404떄리기
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoCreateSerializer(
            todo, data=request.data)  # 수정된 data를 직렬화한후
        if serializer.is_valid():  # 유효검사 진행(데이터 모델의 필드랑 일치하는지도 검사함)
            serializer.save()  # 통과되면 역직렬화(파이썬 객체로 변환시킨다음 데이터베이스에 저장)
            # 통과된 경우 직렬화된 data를 HTTP응답으로 201반환
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 통과하지 못한 경우 HTTP응답으로 400반환
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # 투두 모델에서 특정 투두의 id가 pk와 같다면 todo 변수에 들어감 아니면 404떄리기
        todo = get_object_or_404(Todo, id=pk)
        todo.delete()  # 찾은 데이터를 삭제하기
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoDoneView(APIView):
    def get(self, request):
        dones = Todo.objects.filter(complete=True)  # 완료된 투두 데이터를 가져오고
        serializer = TodoListSerializer(dones, many=True)  # 가져온 데이터를 직렬화한후
        # 직렬화된 serializer.data를 HTTP응답으로 200반환
        return Response(serializer.data, status=status.HTTP_200_OK)


class TodoDetailDoneView(APIView):
    def get(self, request, pk):
        # 투두 모델에서 특정 투두의 id가 pk와 같다면 done 변수에 들어감 아니면 404떄리기
        done = get_object_or_404(Todo, id=pk)
        done.complete = True  # 해당 항목을 완료 상태로 표시하고
        done.save()  # 변경된 데이터를 데이터베이스에 저장
        serializer = TodoDetailSerializer(done)  # 가져온 데이터를 직렬화한후
        return Response(status=status.HTTP_200_OK)  # 200반환

    def delete(self, request, pk):
        # 투두 모델에서 특정 투두의 id가 pk와 같다면 done 변수에 들어감 아니면 404떄리기
        done = get_object_or_404(Todo, id=pk)
        done.delete()  # 찾은 데이터를 삭제하기
        return Response(status=status.HTTP_204_NO_CONTENT)
