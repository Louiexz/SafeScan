from .views import *
import vt
from decouple import config

class view_software(APIView):
    def get(self, request):
        softwareData = Software.objects.all()
        serializer = GetSoftwareSerializer(softwareData, many=True)
        return Response({"message": "All softwares data.", "data": serializer.data},
                        status=status.HTTP_200_OK)

    def post(self, request):
        if request.data.get("name") and request.data.get("status"):
            serializer = CreateSoftwareSerializer(data=request.data)

            if serializer.is_valid():
                name = serializer.validated_data.get("name")

                # Verifica se o software já existe pelo nome
                if Software.objects.filter(name=name).exists():
                    return Response({"message": "Este software já existe."},
                                    status=status.HTTP_401_UNAUTHORIZED)

                # Associa o software ao usuário logado, se estiver autenticado
                if request.user.is_authenticated:
                    serializer.validated_data["user"] = request.user
                else:
                    serializer.validated_data["user"] = None  # Se não estiver logado, o software não tem usuário associado

                serializer.save()
                return Response({"message": "Software criado com sucesso.", "data": serializer.data},
                                 status=status.HTTP_201_CREATED)

        return Response({"message": "Dados inválidos. Inclua 'name' e 'status' para criar um software."},
                        status=status.HTTP_400_BAD_REQUEST)

class view_url_file(APIView):
    def get(self, request):
        return Response({"message": "Check software by: url or file}"}, 
                        status=status.HTTP_200_OK)

    def post(self, request):
        if request.data.get("file") or request.data.get("url"):
            try:
                client = vt.Client(config("API_KEY"))
            except Exception as e:
                return Response({"message": "Not connected with VirusTotal's API."},
                                status=status.HTTP_400_BAD_REQUEST)

            if request.data.get("file"):
                file_name = request.data.get("file")
                try:
                    file = client.get_object(f"/files/{file_name}")
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
                    return Response({"message": "URL searched.", "data": url_data.last_analysis_stats},
                                    status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"message": "Error retrieving URL.", "error": str(e)},
                                    status=status.HTTP_400_BAD_REQUEST)

class delete_software(APIView):
    def delete(self, request, id):
        try:
            # Busca o software pelo UUID
            software = Software.objects.get(id=id)
            software.delete()
            return Response({"message": "Software deleted."}, status=status.HTTP_200_OK)
        except Software.DoesNotExist:
            return Response({"error": "Software not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error deleting software."}, status=status.HTTP_400_BAD_REQUEST)
