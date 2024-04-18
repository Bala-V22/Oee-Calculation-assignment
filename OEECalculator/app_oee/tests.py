from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Machine, ProductionLog
from .views import OeeAPIView
from .utils import calculate_oee_components

class TestOeeAPIView(TestCase):
    def setUp(self):
        self.machine1 = Machine.objects.create(machine_name='Machine 1', machine_serial_no='123456')
        self.machine2 = Machine.objects.create(machine_name='Machine 2', machine_serial_no='789012')

        ProductionLog.objects.create(machine=self.machine1, cycle_no='CN001', unique_id='ID001', material_name='Material 1', start_time='2024-04-01T08:00:00Z', end_time='2024-04-01T10:00:00Z', duration=2)
        ProductionLog.objects.create(machine=self.machine1, cycle_no='CN002', unique_id='ID002', material_name='Material 1', start_time='2024-04-01T08:00:00Z', end_time='2024-04-01T10:00:00Z', duration=5)

        ProductionLog.objects.create(machine=self.machine2, cycle_no='CN003', unique_id='ID003', material_name='Material 2', start_time='2024-04-01T08:00:00Z', end_time='2024-04-01T10:00:00Z', duration=2)
        ProductionLog.objects.create(machine=self.machine2, cycle_no='CN004', unique_id='ID004', material_name='Material 2', start_time='2024-04-01T08:00:00Z', end_time='2024-04-01T10:00:00Z', duration=2)

    def test_oee_api_view(self):
        client = APIClient()
        url = reverse('oee-api') 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 
        self.assertEqual(response.data[0]['machine_name'], 'Machine 1')
        self.assertIn('machine_serial_no', response.data[0])
        self.assertIn('oee', response.data[0])

        # Calculate expected OEE using calculate_oee_components function
        machine1_logs = ProductionLog.objects.filter(machine=self.machine1)
        total_products_machine1 = machine1_logs.count()
        good_products_machine1 = machine1_logs.filter(duration=5).count()

        available_time = 3 * 8  
        ideal_cycle_time = 5 
        available_operating_time = total_products_machine1 * ideal_cycle_time
        unplanned_downtime = available_time - available_operating_time

        availability, performance, quality = calculate_oee_components(
            available_time, unplanned_downtime, ideal_cycle_time, total_products_machine1, good_products_machine1
        )
        expected_oee_machine1 = availability * performance * quality

        self.assertAlmostEqual(response.data[0]['oee'], expected_oee_machine1)
