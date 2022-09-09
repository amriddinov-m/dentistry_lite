from django.contrib import admin

from patient.models import Patient, Record


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass
