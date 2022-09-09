from django.forms import ModelForm

from patient.models import Patient


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
