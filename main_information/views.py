from django.shortcuts import render
from .models import info_main

# Create your views here.
def main1(request):      
    try:
        block = info_main.objects.last()
        bl_1 = block.block_1
        bl_2 = block.block_2
        image_1 = block.image_1
        image_2 = block.image_2
    except (ValueError, NameError, RuntimeError, IOError, TypeError, AttributeError):
        bl_1 = ''
        bl_2 = ''
    blocks ={'block1': bl_1, 'block2': bl_2}
    return render(request, 'information/home.html', blocks)
    



def detail(request,store_id=1,location=None):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    STORE_NAME = 'Downtown'
    store_address = {'street':'Main #385','city':'San Diego','state':'CA'}
    store_amenities = ['WiFi','A/C']
    store_menu = ((0,''),(1,'Drinks'),(2,'Food'))
    vals_for_template = {'store_name':STORE_NAME, 'store_address':store_address, 'store_amenities':store_amenities, 'store_menu':store_menu}
    return render(request,'information/home.html', vals_for_template)

