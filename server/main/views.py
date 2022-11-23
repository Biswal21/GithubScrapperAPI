# from django.shortcuts import render
import requests, math, csv, os
from datetime import datetime
from rest_framework import viewsets, status
import base64

# from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse

from drf_yasg.utils import swagger_auto_schema

from .serializers import GithubUserSerializer, FetchParameterSerialzier
from .models import GithubUser
from main.utils import get_user_profile_urls, get_users_profile_data

# Create your views here.
class FetchViewsets(viewsets.ViewSet):
    @action(detail=False, methods=["post"], url_path="fetch")
    @swagger_auto_schema(
        request_body=FetchParameterSerialzier, responses={200: FetchParameterSerialzier}
    )
    def fetch_and_insert_users(self, request):
        """
        Endpoint for fetching gtihub users based on keyword provided in the request
        """
        serialzed = FetchParameterSerialzier(data=request.data)
        if serialzed.is_valid():
            query_param_str = ""
            for q in serialzed.data["query_keyword"]:
                if q != "":
                    query_param_str += " " + q
            if (
                "location" in list(serialzed.data.keys())
                and serialzed.data["location"] != ""
            ):
                query_param_str += " location:" + serialzed.data["location"]
            for lang in serialzed.data["language"]:
                if lang != "":
                    query_param_str += " language:" + lang
            if serialzed.data["sort"] != "":
                sort_str = serialzed.data["sort"]
            data = {
                "q": query_param_str,
                "sort": sort_str,
                "per_page": "100",
            }
            print(query_param_str)
            token = {"Authorization": "Token " + os.environ.get("GITHUB_TOKEN")}
            try:
                search_response = requests.get(
                    os.environ.get("GITHUB_USER_API"),
                    params=data,
                    headers=token,
                ).json()
            except:
                print("Here")
                return Response(
                    data={"message": "Github API unreachable"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            page_count = math.ceil(search_response["total_count"] / 100)
            all_user_urls = []
            if page_count == 1:
                items = search_response["items"]
                all_user_urls.extend([item["url"] for item in items])
            elif page_count > 1:

                last_page_extra = math.ceil(
                    abs(100 - (page_count - search_response["total_count"] / 100) * 100)
                )
                all_user_urls, is_err, err = get_user_profile_urls(
                    page_count, data, last_page_extra, token
                )
                if is_err == True:
                    return Response(
                        data=err,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            user_profile_data_list, is_err, err = get_users_profile_data(
                all_user_urls, token
            )
            if is_err == True:
                return Response(
                    data=err,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Saving data into DB
            serialzed_data = GithubUserSerializer(
                data=user_profile_data_list, many=True
            )
            if serialzed_data.is_valid():
                serialzed_data.save()
            else:
                return Response(
                    data=serialzed_data.errors,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Generating CSV for the search
            date_time = datetime.now().strftime("D_%m_%d_%Y_T_%H%M%S")
            filename = "user_profiles_{date}.csv".format(date=date_time)
            user_profile_data_list[0]
            with open(filename, "w") as infile:
                writer = csv.DictWriter(
                    infile,
                    fieldnames=list(user_profile_data_list[0].keys()),
                )
                writer.writeheader()
                for user in user_profile_data_list:
                    writer.writerow(user)

            with open(filename, "rb") as infile:
                response = HttpResponse(infile, content_type="text/csv")
                response.status_code = 200
                response[
                    "Content-Disposition"
                ] = 'attachment; filename="{file}"'.format(file=filename)

            return response
        return Response(data=serialzed.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: GithubUserSerializer})
    def read_users(self, request):
        """
        Endpoint for reading all searched yet based on date
        """
        queryset = GithubUser.objects.all()

        try:
            serialized = GithubUserSerializer(instance=queryset, many=True)
        except:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)
