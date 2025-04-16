from django.db import models

class ParkingConfiguration(models.Model):
    name = models.CharField(max_length=100)
    total_spaces = models.IntegerField(default=500)
    min_hourly_spaces = models.IntegerField(default=50)
    occupancy_requirement = models.FloatField(default=0.85)
    
    hourly_revenue = models.FloatField(default=15.0)
    monthly_revenue = models.FloatField(default=10.0)
    corporate_revenue = models.FloatField(default=20.0)
    
    hourly_reliability = models.FloatField(default=0.75)
    monthly_reliability = models.FloatField(default=0.90)
    corporate_reliability = models.FloatField(default=0.60)
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    # Optimization results
    hourly_spaces = models.IntegerField(null=True, blank=True)
    monthly_spaces = models.IntegerField(null=True, blank=True)
    corporate_spaces = models.IntegerField(null=True, blank=True)
    expected_revenue = models.FloatField(null=True, blank=True)
    expected_occupancy = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.name