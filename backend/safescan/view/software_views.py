from .views import *
import vt
from decouple import config

@api_view(["GET", "POST", "PUT"])
def view_software(request):
    if request.method == "GET":
        softwareData = Software.objects.all()
        serializer = SoftwareSerializer(softwareData, many=True)
        return Response({"message":"All softwares data.", "data":serializer.data},
                        status=status.HTTP_200_OK)

    elif request.method == "POST":
        if request.data.get("file") or request.data.get("url"):
            try:
                client = vt.Client(config("API_KEY"))
            except Exception as e:
                return Response({"message":"Not connected with VirusTotal's API."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            if request.data.get("file"):
                file_name = request.data.get("file")
                try:
                    file = client.get_object(f"/files/{file_name}")
                    # Assuming 'file' has a method 'to_dict()' to convert it to a JSON-serializable dict
                    return Response({"message": "File uploaded.", "data": file.to_dict()},
                                    status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"message": "Error retrieving file.", "error": str(e)},
                                    status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get("url"):
                url = request.data.get("url")
                url_id = vt.url_id(url)
                try:
                    url_data = client.get_object(f"/urls/{url_id}")
                    # Assuming 'url_data' has a method 'to_dict()' to convert it to a JSON-serializable dict
                    return Response({"message": "URL searched.", "data": url_data.last_analysis_stats},
                                    status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"message": "Error retrieving URL.", "error": str(e)},
                                    status=status.HTTP_400_BAD_REQUEST)
                
        elif request.data.get("name") and request.data.get("status"):
            # Usar na ia:
            # request.data.get("localizacao_rede")
            # request.data.get("mensagens_chamada")
            # request.data.get("sistema_processos")
            # request.data.get("audio_hardware")
            # request.data.get("armazenamento_externo")

            serializer = SoftwareSerializer(data=request.data)

            if serializer.is_valid():
                name = serializer.validated_data.get("name")

                if Software.objects.filter(name=name).exists():
                    return Response({"message": "Este software já existe."},
                                    status=status.HTTP_401_UNAUTHORIZED)

                if request.user.is_authenticated:
                    serializer.validated_data["user"] = request.user
                
                serializer.save()
                return Response({"message":"Software created sucessfully.", "data":serializer.data
                                 }, status=status.HTTP_201_CREATED)
        return Response({"message":"""Check software by: url, file or boolean questions
(localizacao_rede, mensagens_chamada, sistema_processos, audio_hardware, armazenamento_externo)."""
                        }, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return Response({"message": "Authenticate to update software."},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        software = Software.objects.get(pk=request.data.get('id'), user=request.user)
        serializer = SoftwareSerializer(software, data=request.data)
        
        if serializer.is_valid():
            serializer.user = request.user
            serializer.save()
            return Response({"message":"Software updated sucessfully.", "data":serializer.data},
                            status=status.HTTP_200_OK)
    
    return Response({'message': 'Invalid method.'},
                      status=status.HTTP_405_METHOD_NOT_ALLOWED)