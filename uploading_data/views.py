from django.shortcuts import render

from django.template.context_processors import request

import numpy as np

from .models import xml_intensities, upload_groups, upload

from graphos.sources.simple import SimpleDataSource

from graphos.renderers.gchart import LineChart

from pyspark import SparkConf, SparkContext

from numpy import number

import numbers

import re

import tensorflow

import os

os.environ["PYSPARK_PYTHON"]="/usr/bin/python3.5"

conf = SparkConf()
conf.setMaster("local[4]")
conf.setAppName("Semiconductor_Lab")
conf.set("spark.executor.memory", "1g")
sc = SparkContext(conf = conf)

#from pyspark.conf import SparkConf
#from pyspark.sql import SparkSession
#Spa#ZrkSession.builder.config(conf=SparkConf())

#global variable theta(because of apache spark)
theta = 0

#global name for groups
name_group = ''
name_substrate = ''
# Create your views here.


def retrieveGroups(request):
    
    try:
        flag = True
        groups = upload_groups.objects.all()
        name_group = request.POST.get('iterate_groups')
        name_substrate = request.POST.get('iterate_substrate')
        
        if request.method == 'GET':
           
           context = {'groups': groups}
           return render(request, 'data/retreiveGroups.html', context)
       
        else:
       
            xml_files = upload.objects.filter(file_upl_group__upload_group = name_group, file_upl_group__upload_substrate=name_substrate)
            context = {'xml_files': xml_files, 'name': name_group}
            return render(request, 'data/retreiveFiles.html', context)
        
        context = {'groups': groups}
        return render(request, 'data/retreiveGroups.html', context)
    
    except Exception as e:
        
        template = 'data/viewChartsError.html'
        return render(request, template)
        

def apache_separate_data(intens):
    paralel_data = sc.parallelize([intens.intensities]).flatMap(lambda x: re.split(' ', x.strip()))
    pd_count = paralel_data.count()
    theta2_difer = (intens.endPosition - intens.startPosition)/(pd_count)
    global theta 
    theta = intens.startPosition
     
    def func(x):
        global theta
        theta += theta2_difer
        a = [theta, int(x)]
        return a
      
    data = [['Theta', 'Intensities']]  
    numb = paralel_data.map(func)    
    return numb.collect()


def viewChartData(request, files_name="1"):   
    startP = 0     
    data = [['Theta', 'Intensities']] 
    upl_gr = ''
    xml_files = []
             
    try:
              
        name = request.POST.get('retreive_elements')
        
        if request.method == 'GET':
                
            static_xml_obj = upload.objects.last()
            intens_1 = xml_intensities.objects.get(upload_xml =  static_xml_obj.id)
            startP = intens_1.startPosition
            # apache spark paralellize func
            data1 = apache_separate_data(intens_1)
            # data list for the Chart
            data.extend(data1)
        
        else:
            
            xml_obj = upload.objects.get(name_of_file = name)
            intens_1 = xml_intensities.objects.get(upload_xml = xml_obj.id)
            startP = intens_1.startPosition          
            # apache spark paralellize func        
            data1 = apache_separate_data(intens_1)
            data.extend(data1)
                     
    except Exception as e:
        
        template = 'data/viewChartsError.html'
        return render(request, template)
    
        # DataSource object
    data_source = SimpleDataSource(data=data)
        # Chart object
    chart = LineChart(data_source, width = '950px', options={'title': 'XRD: Theth2 / Intensities'})
    template = 'data/viewCharts.html'
    context = {'chart': chart, 'name': name, 'startP': startP}
    return render(request, template, context)

#not used
def viewChart(request):
    
    intens = xml_intensities.objects.last()
    xml_files = upload.objects.all()
    name = request.POST.get('dropdown1')
    
    # apache spark paralellize func
    paralel_data = sc.parallelize(intens.intensities, 12)
    pd_count = paralel_data.count()
    pd_count /= 5
    numbers = paralel_data.map(lambda line: re.split(' ', line.strip()))
    theta2_difer = (intens.endPosition - intens.startPosition)/(pd_count)
    theta = theta2.startPosition
    count_ch = 1
    i_char = ''
    data = [['Theta', 'Intensities']]
    for i in intens.intensities:
        if i == " ":
            theta += theta2_difer
            d = [theta ,int(i_char)]
            data.append(d)
            i_char = ''
            pd_count -= 1
            count_ch += 1
            
        i_char += i
# DataSource object
    data_source = SimpleDataSource(data=data)
# Chart object
    chart = LineChart(data_source)
    template = 'data/viewChats.html'
    context = {'chart': chart, 'xml_files': xml_files, 'pd_count': pd_count, 'count_ch': count_ch, 'name': name}
    return render(request, 'data/viewCharts.html', context)


