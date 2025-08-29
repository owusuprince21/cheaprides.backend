from django.contrib import admin


from .models import Car, CarImage

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # list_display = ['title', 'make', 'model', 'year', 'price', 'is_featured', 'is_available', 'created_at']
    # list_filter = ['make', 'fuel_type', 'transmission', 'condition', 'is_featured', 'is_available']
    # search_fields = ['title', 'make', 'model', 'description']
    # prepopulated_fields = {'slug': ('title',)}
    # list_editable = ['is_featured', 'is_available']
    # inlines = [CarImageInline]
    
    # fieldsets = (
    #     ('Basic Information', {
    #         'fields': ('title', 'slug', 'description', 'price', 'main_image')
    #     }),
    #     ('Car Specifications', {
    #         'fields': ('make', 'model', 'year', 'mileage', 'fuel_type', 'transmission', 'condition', 'color', 'engine_size', 'doors', 'seats')
    #     }),
    #     ('Features & Status', {
    #         'fields': ('features', 'is_featured', 'is_available')
    #     }),
    # )
    @admin.display(boolean=True, description='Keys')
    def has_keys(self, obj):
        return obj.keys

    list_display = [
        'title', 'make', 'model', 'year', 'price',
        'is_featured', 'is_available', 'created_at',
        'primary_damage', 'drive', 'body_style', 'has_keys'  # optional new fields for display
    ]
    list_filter = [
        'make', 'fuel_type', 'transmission', 'condition',
        'is_featured', 'is_available', 'drive', 'body_style'
    ]
    search_fields = ['title', 'make', 'model', 'description', 'primary_damage']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_available']
    inlines = [CarImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'price', 'main_image')
        }),
        ('Car Specifications', {
            'fields': (
                'make', 'model', 'year', 'mileage', 'fuel_type',
                'transmission', 'condition', 'color', 'engine_size',
                'doors', 'seats', 'drive', 'body_style'
            )
        }),
        ('Damage & Keys', {
            'fields': ('primary_damage', 'keys')
        }),
        ('Features & Status', {
            'fields': ('features', 'is_featured', 'is_available')
        }),
    )

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'caption', 'created_at']
    list_filter = ['created_at']

