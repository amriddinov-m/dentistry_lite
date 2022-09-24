from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from patient.models import Patient
from patient.serializers import PatientListSerializer


class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        phone = self.request.query_params.get('phone')
        chat_id = self.request.query_params.get('chat_id')
        queryset = Patient.objects.filter(phone=f'+{phone}')
        if queryset:
            queryset.update(chat_id=chat_id)
        return queryset
