from django.contrib import admin
from .models import User, Signature, VerificationLog

admin.site.register(User)
admin.site.register(Signature)
admin.site.register(VerificationLog)
