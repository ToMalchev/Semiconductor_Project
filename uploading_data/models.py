from django.db import models

from django.utils.encoding import python_2_unicode_compatible

from django.dispatch import receiver

from django.db.models.signals import post_save

import xml.etree.ElementTree as ET

from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _

import re

#.xrdml validator
def validate_file(value):
    result = re.match(r'.*.xrdml', value.name)
    
    if not result:
        raise ValidationError(
            _('%(value)s is not an xrdml(xml) file'),
            params={'value': value},
        )


def validate_group(value):
    
    if value == "":
        raise ValidationError("Please add or choose group")

        
# Good or Bad quality of the data 
class training(models.Model):
    good_growth = models.BooleanField(default = False)
    
    def __str__(self):
        return '%s' % self.good_growth
    
    
# Model for the groups of the growths
class upload_groups(models.Model):
    upload_group = models.CharField(max_length=40)
    upload_substrate = models.CharField(max_length=40, default='', blank = True)
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return "%s %s" % (self.upload_group, self.upload_substrate) 


# Model for uploading data(xml files)
class upload(models.Model):
    name_of_file = models.CharField(max_length=40, default='xml file', unique=1)
    xml_files = models.FileField(upload_to="upload_xml_files", validators=[validate_file])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    file_upl_group = models.ForeignKey(upload_groups, on_delete=models.CASCADE, default='', validators=[validate_group])
    ext_training = models.ForeignKey(training, on_delete=models.CASCADE, default=False)
    
    def __str__(self):
        return "%s" % self.name_of_file
#     def __save__(self):
#         u = super(User, self).save(*args, **kwargs)
#         tree = ET.parse(u.xml_files)
#         root = tree.getroot()
#         xrdMeasurement = root.find('{http://www.xrdml.com/XRDMeasurement/1.3}xrdMeasurement')
#         scan = xrdMeasurement.find('{http://www.xrdml.com/XRDMeasurement/1.3}scan')
#         dataPoints = scan.find('{http://www.xrdml.com/XRDMeasurement/1.3}dataPoints')
# 
#         intensities_child = dataPoints.find('{http://www.xrdml.com/XRDMeasurement/1.3}intensities').text
#         xml_intensities.objects.get_or_create(xml_intensities_id=u.id, intensities = "intensities_child")
#         
#         positions = dataPoints.find('{http://www.xrdml.com/XRDMeasurement/1.3}positions')        
#         theta_start_position = float(positions.find('startPositoin').text)
#         theta_end_position = float(positions.find('endPosition').text)
#         xml_2Theta.objects.get_or_create(xml_2Theta_id = u.id, startPosition = theta_start_position, endPosition = theta_end_position) 
#         return u # save needs to return a `User` object, remember!


# Model for the data extracted from the xml
class xml_intensities(models.Model):
    upload_xml = models.OneToOneField(upload, on_delete=models.CASCADE)
    intensities = models.TextField()    
    startPosition = models.FloatField(default=None)
    endPosition = models.FloatField(default=None)
    
    def __str__(self):
        return "%s" % self.upload_xml
    
 
#Creating xml_intensities objects and xml_2Theta
@receiver(post_save, sender=upload)  
def extracting_data_from_xml(sender,instance, **kwargs):
    
    if kwargs.get('created', True):        
        
        tree = ET.parse(instance.xml_files)
        root = tree.getroot()
        xrdMeasurement = root.find('{http://www.xrdml.com/XRDMeasurement/1.3}xrdMeasurement')
        scan = xrdMeasurement.find('{http://www.xrdml.com/XRDMeasurement/1.3}scan')
        dataPoints = scan.find('{http://www.xrdml.com/XRDMeasurement/1.3}dataPoints')
    
        intensities_child = dataPoints.find('{http://www.xrdml.com/XRDMeasurement/1.3}intensities').text
            
        positions = dataPoints.find('{http://www.xrdml.com/XRDMeasurement/1.3}positions')        
            
        theta_start_position = float(positions.find('{http://www.xrdml.com/XRDMeasurement/1.3}startPosition').text)
        theta_end_position = float(positions.find('{http://www.xrdml.com/XRDMeasurement/1.3}endPosition').text)
        xml_intensities.objects.get_or_create(upload_xml_id=instance.id, intensities = intensities_child, startPosition=theta_start_position, endPosition=theta_end_position)
   
        
        
        