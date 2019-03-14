from django.contrib import admin

from apps.engineering.models import Project, ProjectFile, ProjectBudget, ProjectEquipment, ProjectBid, ProjectQuote, \
    ProjectQuoteItem

admin.site.register(Project)
admin.site.register(ProjectFile)
admin.site.register(ProjectBudget)
admin.site.register(ProjectEquipment)
admin.site.register(ProjectBid)
admin.site.register(ProjectQuote)
admin.site.register(ProjectQuoteItem)