from .views import *

import os

@api_view(["GET", "PUT"])
def view_profile(request):
    profileData = User.objects.filter(user=request.user)

    if request.method == "GET":
        serializer = UserSerializer(profileData, many=True)

        return Response({"message":"All user profile data."}, data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = UserSerializer(profileData, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Profile updated sucessfully."}, data=serializer.data, status=status.HTTP_200_OK)
    
    #if request.method == "DELETE":
    #    profileData.delete()
    #    return Response({'message': 'Profile deleted successfully.'},
    #                  status=status.HTTP_204_NO_CONTENT)

    return Response({'message': 'Invalid method.'},
                      status=status.HTTP_405_METHOD_NOT_ALLOWED)
