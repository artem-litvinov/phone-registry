from django.contrib.auth.models import User, Group
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request

from numbers_app.serializers import (
    UserSerializer,
    GroupSerializer,
)
from numbers_app.models import RegistryEntry
from numbers_app.forms import PhoneNumberForm


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def get_phone(request):
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            try:
                code = int(form.cleaned_data["code"])
                number = int(form.cleaned_data["number"])
            except ValueError as e:
                return HttpResponseBadRequest(e)

            phone = RegistryEntry.objects.filter(code=code, min_number__lte=number, max_number__gte=number).first()

            if phone:
                phone_info = dict(
                    code=form.cleaned_data["code"],
                    number=form.cleaned_data["number"],
                    operator=phone.operator,
                    region=phone.region,
                )
                return render(request, "phone.html", {"form": form, "phone_info": phone_info})
            
            return render(request, "phone.html", {"form": form, "no_such_phone": True})
            

    else:
        form = PhoneNumberForm()

    return render(request, "phone.html", {"form": form})
