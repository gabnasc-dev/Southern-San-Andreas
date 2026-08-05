from django.contrib import admin
from cars.models import Car, CarPhoto, Brand, CarInventory


class CarPhotoInline(admin.TabularInline):
    model = CarPhoto
    extra = 1
    fields = ('image', 'position')


class CarAdmin(admin.ModelAdmin):
    list_display = (
        "modelCar", "brandCar", "factoryYear", "mileage", "valueCar",
        "carStatus", "carOwner",
    )
    # brandCar e uma FK: buscar por ela exige o lookup do campo de texto,
    # senao o admin levanta "Related Field got invalid lookup: icontains".
    search_fields = ("modelCar", "brandCar__nameBrand", "plateCar", "color")
    list_filter = ("carStatus", "transmission", "fuel", "brandCar", "factoryYear")
    list_select_related = ("brandCar", "carOwner")
    autocomplete_fields = ("brandCar",)
    inlines = [CarPhotoInline]


class BrandAdmin(admin.ModelAdmin):
    list_display = ("idBrand", "nameBrand",)
    search_fields = ("nameBrand",)


class CarInventoryAdmin(admin.ModelAdmin):
    list_display = ("createdAt", "carsCount", "carsValue")
    readonly_fields = ("createdAt",)


admin.site.register(Car, CarAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(CarInventory, CarInventoryAdmin)

admin.site.site_header = 'Southern San Andreas'
admin.site.site_title = 'Southern San Andreas'
admin.site.index_title = 'Administração'
