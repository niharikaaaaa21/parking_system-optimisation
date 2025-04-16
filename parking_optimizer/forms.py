from django import forms
from .models import ParkingConfiguration

class ParkingConfigForm(forms.ModelForm):
    class Meta:
        model = ParkingConfiguration
        fields = [
            'name', 'total_spaces', 'min_hourly_spaces', 'occupancy_requirement',
            'hourly_revenue', 'monthly_revenue', 'corporate_revenue',
            'hourly_reliability', 'monthly_reliability', 'corporate_reliability'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_spaces': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_hourly_spaces': forms.NumberInput(attrs={'class': 'form-control'}),
            'occupancy_requirement': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'hourly_revenue': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monthly_revenue': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'corporate_revenue': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'hourly_reliability': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'monthly_reliability': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'corporate_reliability': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
        }
        
        labels = {
            'name': 'Configuration Name',
            'total_spaces': 'Total Parking Spaces',
            'min_hourly_spaces': 'Minimum Hourly Spaces Required',
            'occupancy_requirement': 'Required Occupancy Rate (0-1)',
            'hourly_revenue': 'Hourly Space Revenue ($/day)',
            'monthly_revenue': 'Monthly Permit Revenue ($/day)',
            'corporate_revenue': 'Corporate Space Revenue ($/day)',
            'hourly_reliability': 'Hourly Space Occupancy Rate (0-1)',
            'monthly_reliability': 'Monthly Permit Occupancy Rate (0-1)',
            'corporate_reliability': 'Corporate Space Occupancy Rate (0-1)',
        }