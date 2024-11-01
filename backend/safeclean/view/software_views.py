from .views import *

@api_view(["GET", "POST", "PUT", "DELETE"])
def view_software(request):
    softwareData = Software.objects.filter(user=request.user)

    if request.method == "GET":
        serializer = SoftwareSerializer(softwareData, many=True)

        return Response({"message":"All user software data."}, data=serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = SoftwareSerializer(softwareData, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Software created sucessfully."}, data=serializer.data, status=status.HTTP_201_CREATED)
    
    if request.method == "PUT":
        software = softwareData.objects.get(pk=request.data.get('id'))
        serializer = SoftwareSerializer(software, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Software updated sucessfully."}, data=serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "DELETE":
        software = softwareData.objects.get(pk=request.data.get('id'))
        software.delete()
        return Response({'message': 'Software deleted successfully.'},
                      status=status.HTTP_204_NO_CONTENT)