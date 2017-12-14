from django.shortcuts import render

import numpy as np

from uploading_data.models import xml_intensities, upload, upload_groups

from pyspark import SparkConf

from pyspark.sql.types import *

from pyspark.sql.functions import *

from pyspark.sql import Row

from pyspark.ml.linalg import Vectors, VectorUDT

from pyspark.ml.feature import VectorAssembler

from pyspark.ml.classification import MultilayerPerceptronClassifier

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from numpy import number as np

import numbers

import re

import numpy

from uploading_data.views import sc, apache_separate_data
#spark set up

theta = 0

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession, SQLContext
# SparkSession.builder.config(conf=SparkConf())
# sqlContext = SQLContext(sc)

spark = SparkSession \
    .builder \
    .appName("SemiconductorLab") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()


# Create your views here.
def neural_net(request):
    name_group = request.POST.get('analize_list')
    xml_files = upload.objects.filter(file_upl_group__upload_group = name_group) 
    intensities = xml_intensities.objects.all()
    dList = spark.createDataFrame(intensities)
    #dList = dataframe.rdd.map(apache_separate_data)
    select_list = dList.select(dList['intensities'])
    dList.createOrReplaceTempView("dList")
    name_group = request.POST.get('analize_list')
            
    # With only one parameter - elements are not separated
    def df_extract(x):
        intens = re.split(' ', x[0])
          
        count = len(intens)
        theta_dif = (x[2] - x[1])/count
        theta = x[1]
        s = []
        j = 0
        for i in intens:
            theta += theta_dif
            v = Vectors.dense(theta, int(i))
            j += 1
            s.append(Row(j, v))
        a = []
        a.extend(s)
        return a
    
    # 3 parameters - elements are separated 
    def df_extract_1(x,y,z):
        intens = re.split(' ', x)
          
        count = len(intens)
        theta_dif = (z - y)/count
        theta = y
        s = []
        j = 0
        for i in intens:
            theta += theta_dif
            v = Vectors.dense(theta, int(i))
            j += 1
            s.append(Row(j, v))
        a = []
        a.extend((s))
        return a
    
    #convert to VectorDense
    def df_vector(x):
        dulug = len(x[0])
        s = []
        i = 0
        for i in range(dulug):
            v = Vectors.dense(x[0][i][0], x[0][i][1])
            i += 1
            s.append((i,(v)))
        a = [(s)]
        return ((s))
    #list_inten = spark.sql('SELECT intensities, 8startPosition, endPosition FROM dList').rdd.map(df_extract).toDF()
    
    # Работещ !!!
    #list_inten = spark.sql('SELECT intensities, startPosition, endPosition FROM dList').rdd.map(lambda x: Row(df_extract_1(x[0], x[1], x[2]))).toDF(['features'])
    
    list_inten = spark.sql('SELECT intensities, startPosition, endPosition FROM dList').rdd.map(lambda x: df_extract_1(x[0], x[1], x[2]))#.toDF(['label', 'features'])
    
    #list_inten = list_inten.map(lambda x: x).toDF(['dsd', 'ebalo si e'])
    
    struct_schema = ArrayType(StructType([StructField("label", LongType()), StructField("features", VectorUDT())]))
    list_inten_df = spark.createDataFrame(list_inten, schema = struct_schema)
    
    list_inten_df.createOrReplaceTempView("list_inten_df")    

   #SS vecAssembler = VectorAssembler(inputCols=["features"], outputCol="features")
   # zavurshen = vecAssembler.transform(list_inten_df).head().features

    #list_inten = list_inten.map((df_vector))
    

#     cSchema = StructType([StructField('field', StructType([StructField('label', IntegerType(), True), StructField('features', VectorUDT(), True)]), True)])
#   
#     list_inten= spark.createDataFrame(list_inten, schema = cSchema)
    #list_inten = list_inten.map(lambda x: Vectors.dense(x[0][5][1]))
    
    
    # specify layers for the neural network:
    # input layer of size 4 (features), two intermediate of size 5 and 4
    # and output of size 3 (classes)
    layers = [1219, 25, 14, 1]
#      
    trainer = MultilayerPerceptronClassifier(maxIter=100, layers=layers, blockSize=128, seed=1234)
# #     
    model = trainer.fit(list_inten_df)


    #list_inten = spark.sql('SELECT intensities, startPosition, endPosition FROM dList').rdd.map(lambda x: re.split(" ", x[0]))
    
#     start_pos = spark.sql('SELECT startPosition FROM dList')[0]
#     end_pos = spark.sql('SELECT endPosition FROM dList')[0]
    
    #list_inten = dList.rdd.map(lambda x: (re.split(' ', x[0]),int(x[2]) - int(x[1])))
         
    
    #list_inten = list_inten.toDF(['theta2', 'intensities'])
    list_inten = list_inten_df.collect()
#    list_inten = 'It is still under development'
    context = {'Data_Frame': list_inten, 'select_list': select_list, 'xml_files': xml_files}
    
    return render(request, 'analize_data/analize.html', context)
    

def data_analize(request):
    
    group = []
    name_group = request.POST.get('analize_list')
    name_substrate = request.POST.get('iterate_substrate')
    groups = upload_groups.objects.all()
    
    
    
    if request.method=='POST':
        flag = True
        xml_files = upload.objects.filter(file_upl_group__upload_group = name_group, file_upl_group__upload_substrate=name_substrate)
        intensities = xml_intensities.objects.all()
        dataframe = spark.createDataFrame(intensities)
        i = dataframe.select(dataframe.intensities)
        
        context = {'xml_files': xml_files, 'name': i, 'flag': flag}
        return render(request, 'analize_data/analize.html', context)
    
    flag = False
    context = {'groups': groups, 'flag': flag}
    return render(request, 'analize_data/analize.html', context)

