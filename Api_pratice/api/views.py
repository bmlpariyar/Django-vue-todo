from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime
from .serializers import Todo_ListSerializer
from to_do.models import Todo_List


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_lists(request):
  apis = [
    {
      'route': '/api',
      'method': 'GET',
      'description': 'List all APIs',
    },
    {
      'route': '/api/get_time',
      'method': 'GET',
      'description': 'Get current time',
    },
    {
      'route': '/api/todos',
      'method': 'GET',
      'description': 'List all of todos',
    },
    {
      'route': '/api/get_todo/<str:id>',
      'method': 'GET',
      'description': 'Get specified todo of given id',
    },
    {
      'route': '/api/create_todo/',
      'method': 'POST',
      'description': 'Create a new todo on given input',
      'sample_json': {
        'user': 1,
        'title': 'Example title',
        'description': 'Example description'
      }
    },
    {
      'route': '/api/update_todo/<str:id>',
      'method': ['PUT', 'PATCH'],
      'description': 'Update the content of todo based on given id',
    },
    {
      'route': '/api/delete_todo/<str:id>',
      'method': 'DELETE',
      'description': 'Deletes the todo based on given id',
    },
    {
      'route': '/api/token/',
      'method': 'GET',
      'description': 'Get access and refresh token',
    },{
      'route': '/api/token/refresh/',
      'method': 'GET',
      'description': 'Get refresh token',
    },
    
  ]
  return Response(apis)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_time(request):
  return Response({'time': datetime.now().strftime("%Y-%m-%d %H:%M")})
  
  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def to_dos(request):
  todo = Todo_List.objects.filter()
  serializer = Todo_ListSerializer(todo, many=True)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_todo(request, pk):
  todo = Todo_List.objects.get(id=pk)
  serializer = Todo_ListSerializer(todo)
  return Response(serializer.data)



from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_todo(request):
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = Todo_ListSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Data saved successfully", 
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_todo(request, pk):
    todo = Todo_List.objects.get(id=pk)
    serializer = Todo_ListSerializer(todo, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def delete_todo(request, pk):
  try:
    todo = Todo_List.objects.get(id=pk)
  except:
    return Response({'error': 'Cant find the item with given id'}, status=status.HTTP_404_NOT_FOUND)
  if request.method == 'DELETE':
    todo.delete()
    return Response({'message': 'Successfully deleted the todo'}, status=status.HTTP_200_OK)
  else:
    return Response({'error': 'Please pass in the delete method'}, status=status.HTTP_400_BAD_REQUEST)
    