from rest_framework import viewsets
from .models import Machine, ProductionLog
from .serializers import MachineSerializer, ProductionLogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import *

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class ProductionLogViewSet(viewsets.ModelViewSet):
    queryset = ProductionLog.objects.all()
    serializer_class = ProductionLogSerializer

class OeeAPIView(APIView):
    def get(self, request, format=None):
        machines = Machine.objects.all()
        oee_data = []

        for machine in machines:
            production_logs = ProductionLog.objects.filter(machine=machine)

            total_products = production_logs.count()
            good_products = production_logs.filter(duration=5).count()

            available_time = 3 * 8  
            ideal_cycle_time = 5 
            available_operating_time = total_products * ideal_cycle_time
            unplanned_downtime = available_time - available_operating_time

            availability, performance, quality = calculate_oee_components(
                available_time, unplanned_downtime, ideal_cycle_time, total_products, good_products
            )
            print(available_time, unplanned_downtime, ideal_cycle_time, total_products, good_products)
            print(availability, performance, quality)

            if total_products != 0:
                oee = availability * performance * quality
            else:
                oee = 0 

            oee_data.append({
                'machine_name': machine.machine_name,
                'machine_serial_no': machine.machine_serial_no,
                'oee': oee
            })

        return Response(oee_data)

    


import random
import pandas as pd
import pandas as pd
from datetime import datetime
import random

def upload_production_logs_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        machines = Machine.objects.all()


        for index, row in df.iterrows():

            machine = random.choice(machines)

            production_log = ProductionLog(
                machine=machine,
                cycle_no=row['cycle_no'],
                unique_id=row['unique_id'],
                material_name=row['material_name'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                duration=row['duration'],
            )
   
            production_log.save()

        return True, None 
    except Exception as e:
        return False, str(e) 

# Usage example:
# Call this function with the file path of the CSV file
# success, error_message = upload_production_logs_from_csv('app_oee/production_logs.csv')
# if success:
#     print("Production logs uploaded successfully.")
# else:
#     print("Error uploading production logs:", error_message)
