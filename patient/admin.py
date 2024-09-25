from django.contrib import admin

from patient.models import Patient, Appointment, PatientSource


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(PatientSource)
class PatientSourceAdmin(admin.ModelAdmin):
    pass
