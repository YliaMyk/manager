from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.models.models import Task
from api.serializers import TaskSerializer, RegisterSerializer


@swagger_auto_schema(method='post', request_body=TaskSerializer)
@swagger_auto_schema(method='get', responses={200: TaskSerializer})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):

    request_serializer: TaskSerializer
    response_serializer: TaskSerializer

    if request.method == 'GET':
        queryset = Task.objects.filter(owner=request.user)

        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='put', request_body=TaskSerializer)
@swagger_auto_schema(method='get', responses={200: TaskSerializer})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_item(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except:
        return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if not task.owner == request.user:
        return Response({'message': 'You are not a owner of this task.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = TaskSerializer(instance=task, data=request.data)

        if not request.data:
            return Response({'message': 'No data to update'}, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task was deleted successfully!'}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
        "message": "User Created Successfully.  Now perform Login to get your token",
    })