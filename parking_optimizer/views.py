from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

from .models import ParkingConfiguration
from .forms import ParkingConfigForm
from .optimizer import optimize_parking_allocation

def home(request):
    """Home page with list of configurations and form to create new one"""
    configurations = ParkingConfiguration.objects.all().order_by('-date_created')
    
    if request.method == 'POST':
        form = ParkingConfigForm(request.POST)
        if form.is_valid():
            config = form.save()
            messages.success(request, 'Configuration created! Now optimize it.')
            return redirect('optimize', config_id=config.id)
    else:
        form = ParkingConfigForm()
    
    context = {
        'configurations': configurations,
        'form': form
    }
    return render(request, 'parking_optimizer/home.html', context)

def optimize(request, config_id):
    """Optimize a specific configuration"""
    config = get_object_or_404(ParkingConfiguration, id=config_id)
    
    if request.method == 'POST':
        # Run the optimization
        result = optimize_parking_allocation(config)
        
        if result['success']:
            # Save the optimization results
            config.hourly_spaces = result['hourly_spaces']
            config.monthly_spaces = result['monthly_spaces']
            config.corporate_spaces = result['corporate_spaces']
            config.expected_revenue = result['expected_revenue']
            config.expected_occupancy = result['expected_occupancy']
            config.save()
            
            messages.success(request, 'Optimization successful!')
        else:
            messages.error(request, result['message'])
        
        return redirect('results', config_id=config.id)
    
    return render(request, 'parking_optimizer/optimize.html', {'config': config})

def results(request, config_id):
    """Display optimization results"""
    config = get_object_or_404(ParkingConfiguration, id=config_id)
    
    # Check if optimization has been run
    if config.hourly_spaces is None:
        messages.warning(request, 'This configuration has not been optimized yet.')
        return redirect('optimize', config_id=config.id)
    
    # Generate visualization
    pie_chart = generate_allocation_chart(config)
    revenue_chart = generate_revenue_chart(config)
    
    context = {
        'config': config,
        'pie_chart': pie_chart,
        'revenue_chart': revenue_chart,
    }
    
    return render(request, 'parking_optimizer/results.html', context)

def edit_config(request, config_id):
    """Edit an existing configuration"""
    config = get_object_or_404(ParkingConfiguration, id=config_id)
    
    if request.method == 'POST':
        form = ParkingConfigForm(request.POST, instance=config)
        if form.is_valid():
            # Reset optimization results
            config = form.save(commit=False)
            config.hourly_spaces = None
            config.monthly_spaces = None
            config.corporate_spaces = None
            config.expected_revenue = None
            config.expected_occupancy = None
            config.save()
            
            messages.success(request, 'Configuration updated! You need to optimize again.')
            return redirect('optimize', config_id=config.id)
    else:
        form = ParkingConfigForm(instance=config)
    
    return render(request, 'parking_optimizer/edit_config.html', {'form': form, 'config': config})

def delete_config(request, config_id):
    """Delete a configuration"""
    config = get_object_or_404(ParkingConfiguration, id=config_id)
    
    if request.method == 'POST':
        config.delete()
        messages.success(request, 'Configuration deleted successfully.')
        return redirect('home')
    
    return render(request, 'parking_optimizer/delete_config.html', {'config': config})

def generate_allocation_chart(config):
    """Generate pie chart of space allocation"""
    labels = ['Hourly', 'Monthly', 'Corporate']
    sizes = [config.hourly_spaces, config.monthly_spaces, config.corporate_spaces]
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Optimal Parking Space Allocation')
    
    # Save figure to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Convert to base64 for HTML embedding
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    return chart_data

def generate_revenue_chart(config):
    """Generate bar chart of expected revenue by category"""
    categories = ['Hourly', 'Monthly', 'Corporate']
    revenues = [
        config.hourly_spaces * config.hourly_revenue * config.hourly_reliability,
        config.monthly_spaces * config.monthly_revenue * config.monthly_reliability,
        config.corporate_spaces * config.corporate_revenue * config.corporate_reliability
    ]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(categories, revenues, color=['#ff9999', '#66b3ff', '#99ff99'])
    ax.set_ylabel('Expected Daily Revenue ($)')
    ax.set_title('Expected Revenue by Parking Type')
    
    # Add revenue value labels on top of bars
    for i, v in enumerate(revenues):
        ax.text(i, v + 5, f'${v:.2f}', ha='center')
    
    # Save figure to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Convert to base64 for HTML embedding
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    return chart_data