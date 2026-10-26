
from django.contrib import admin
from .models import Species, Breed, Location, Animal, AdoptionRequest


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'species')
    list_filter = ('species',)
    search_fields = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    search_fields = ('name', 'city')


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'species', 'breed', 'location', 'gender', 'status'
    )
    list_filter = ('species', 'gender', 'status', 'location')
    search_fields = ('name', 'description')


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = (
        'animal', 'applicant', 'status', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('animal__name', 'applicant__username')
    list_editable = ('status',)
    ordering = ('-created_at',)
