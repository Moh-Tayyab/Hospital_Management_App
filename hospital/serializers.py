from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Department, Doctor, Nurse, Staff, Patient,
    Appointment, MedicalRecord
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'description']
        extra_kwargs = {
            'description': {'write_only': True}
        }

class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=False)
    department = serializers.CharField(write_only=True, required=False)
    contact_info = serializers.CharField(required=False)
    schedule = serializers.CharField(required=False)
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'department', 'contact_info', 'schedule']
    
    def validate(self, data):
        # Only validate fields that are being updated
        if 'name' in data and not data['name']:
            raise serializers.ValidationError({"name": "Name cannot be empty"})
        if 'department' in data and not data['department']:
            raise serializers.ValidationError({"department": "Department cannot be empty"})
        if 'contact_info' in data and not data['contact_info']:
            raise serializers.ValidationError({"contact_info": "Contact info cannot be empty"})
        if 'schedule' in data and not data['schedule']:
            raise serializers.ValidationError({"schedule": "Schedule cannot be empty"})
        return data
    
    def create(self, validated_data):
        try:
            name = validated_data.pop('name')
            department_name = validated_data.pop('department')
            
            # Create or get department
            try:
                department = Department.objects.get(name=department_name)
            except Department.DoesNotExist:
                department = Department.objects.create(name=department_name)
            
            # Create user
            name_parts = name.split()
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            username = name.lower().replace(' ', '_')
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                username = f"{username}_{User.objects.count()}"
            
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create doctor
            doctor = Doctor.objects.create(
                user=user,
                department=department,
                **validated_data
            )
            return doctor
            
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def update(self, instance, validated_data):
        try:
            # Update name if provided
            if 'name' in validated_data:
                name = validated_data.pop('name')
                name_parts = name.split()
                first_name = name_parts[0]
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                
                instance.user.first_name = first_name
                instance.user.last_name = last_name
                instance.user.save()
            
            # Update department if provided
            if 'department' in validated_data:
                department_name = validated_data.pop('department')
                try:
                    department = Department.objects.get(name=department_name)
                except Department.DoesNotExist:
                    department = Department.objects.create(name=department_name)
                instance.department = department
            
            # Update contact_info if provided
            if 'contact_info' in validated_data:
                instance.contact_info = validated_data.pop('contact_info')
            
            # Update schedule if provided
            if 'schedule' in validated_data:
                instance.schedule = validated_data.pop('schedule')
            
            instance.save()
            return instance
            
        except Exception as e:
            raise serializers.ValidationError(str(e))

class NurseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=False)
    department = serializers.DictField(write_only=True, required=False)
    contact_info = serializers.CharField(required=False)
    shift = serializers.CharField(required=False)
    
    class Meta:
        model = Nurse
        fields = ['id', 'name', 'department', 'contact_info', 'shift']
    
    def validate(self, data):
        if 'name' in data and not data['name']:
            raise serializers.ValidationError({"name": "Name cannot be empty"})
        if 'department' in data:
            department_data = data['department']
            if not department_data.get('name') and not department_data.get('floor'):
                raise serializers.ValidationError({"department": "Either name or floor must be provided"})
        if 'contact_info' in data and not data['contact_info']:
            raise serializers.ValidationError({"contact_info": "Contact info cannot be empty"})
        if 'shift' in data and not data['shift']:
            raise serializers.ValidationError({"shift": "Shift cannot be empty"})
        return data
    
    def create(self, validated_data):
        try:
            name = validated_data.pop('name')
            department_data = validated_data.pop('department')
            
            # Create or get department
            try:
                department = Department.objects.get(name=department_data['name'])
            except Department.DoesNotExist:
                department = Department.objects.create(
                    name=department_data['name'],
                    description=department_data.get('floor', '')
                )
            
            # Create user
            name_parts = name.split()
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            username = name.lower().replace(' ', '_')
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                username = f"{username}_{User.objects.count()}"
            
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create nurse
            nurse = Nurse.objects.create(
                user=user,
                department=department,
                **validated_data
            )
            return nurse
            
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def update(self, instance, validated_data):
        try:
            # Update name if provided
            if 'name' in validated_data:
                name = validated_data.pop('name')
                name_parts = name.split()
                first_name = name_parts[0]
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                
                instance.user.first_name = first_name
                instance.user.last_name = last_name
                instance.user.save()
            
            # Update department if provided
            if 'department' in validated_data:
                department_data = validated_data.pop('department')
                department = instance.department
                
                # Update department name if provided
                if 'name' in department_data and department_data['name']:
                    try:
                        new_department = Department.objects.get(name=department_data['name'])
                        instance.department = new_department
                    except Department.DoesNotExist:
                        # Create new department with existing floor if available
                        new_department = Department.objects.create(
                            name=department_data['name'],
                            description=department.description
                        )
                        instance.department = new_department
                
                # Update department floor if provided
                if 'floor' in department_data and department_data['floor']:
                    instance.department.description = department_data['floor']
                    instance.department.save()
            
            # Update contact_info if provided
            if 'contact_info' in validated_data:
                instance.contact_info = validated_data.pop('contact_info')
            
            # Update shift if provided
            if 'shift' in validated_data:
                instance.shift = validated_data.pop('shift')
            
            instance.save()
            return instance
            
        except Exception as e:
            raise serializers.ValidationError(str(e))

class StaffSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=False)
    department = serializers.DictField(write_only=True, required=False)
    contact_info = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    
    class Meta:
        model = Staff
        fields = ['id', 'name', 'department', 'contact_info', 'role']
    
    def validate(self, data):
        if 'name' in data and not data['name']:
            raise serializers.ValidationError({"name": "Name cannot be empty"})
        if 'department' in data:
            department_data = data['department']
            if not department_data.get('name') and not department_data.get('floor'):
                raise serializers.ValidationError({"department": "Either name or floor must be provided"})
        if 'contact_info' in data and not data['contact_info']:
            raise serializers.ValidationError({"contact_info": "Contact info cannot be empty"})
        if 'role' in data and not data['role']:
            raise serializers.ValidationError({"role": "Role cannot be empty"})
        return data
    
    def create(self, validated_data):
        try:
            name = validated_data.pop('name')
            department_data = validated_data.pop('department')
            
            # Create or get department
            try:
                department = Department.objects.get(name=department_data['name'])
            except Department.DoesNotExist:
                department = Department.objects.create(
                    name=department_data['name'],
                    description=department_data.get('floor', '')
                )
            
            # Create user
            name_parts = name.split()
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            username = name.lower().replace(' ', '_')
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                username = f"{username}_{User.objects.count()}"
            
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create staff
            staff = Staff.objects.create(
                user=user,
                department=department,
                **validated_data
            )
            return staff
            
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def update(self, instance, validated_data):
        try:
            # Update name if provided
            if 'name' in validated_data:
                name = validated_data.pop('name')
                name_parts = name.split()
                first_name = name_parts[0]
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                
                instance.user.first_name = first_name
                instance.user.last_name = last_name
                instance.user.save()
            
            # Update department if provided
            if 'department' in validated_data:
                department_data = validated_data.pop('department')
                department = instance.department
                
                # Update department name if provided
                if 'name' in department_data and department_data['name']:
                    try:
                        new_department = Department.objects.get(name=department_data['name'])
                        instance.department = new_department
                    except Department.DoesNotExist:
                        # Create new department with existing floor if available
                        new_department = Department.objects.create(
                            name=department_data['name'],
                            description=department.description
                        )
                        instance.department = new_department
                
                # Update department floor if provided
                if 'floor' in department_data and department_data['floor']:
                    instance.department.description = department_data['floor']
                    instance.department.save()
            
            # Update contact_info if provided
            if 'contact_info' in validated_data:
                instance.contact_info = validated_data.pop('contact_info')
            
            # Update role if provided
            if 'role' in validated_data:
                instance.role = validated_data.pop('role')
            
            instance.save()
            return instance
            
        except Exception as e:
            raise serializers.ValidationError(str(e))

class PatientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=False)
    age = serializers.IntegerField(required=False)
    gender = serializers.ChoiceField(choices=['M', 'F', 'O'], required=False)
    contact_info = serializers.CharField(required=False)
    medical_history = serializers.CharField(required=False)
    assigned_doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        required=False,
        allow_null=True
    )
    assigned_nurse = serializers.PrimaryKeyRelatedField(
        queryset=Nurse.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'contact_info', 'medical_history', 'assigned_doctor', 'assigned_nurse']
    
    def validate(self, data):
        # Only validate fields that are being updated
        if 'name' in data and not data['name']:
            raise serializers.ValidationError({"name": "Name cannot be empty"})
        if 'age' in data and (data['age'] is None or data['age'] < 0):
            raise serializers.ValidationError({"age": "Age must be a positive number"})
        if 'gender' in data and data['gender'] not in ['M', 'F', 'O']:
            raise serializers.ValidationError({"gender": "Gender must be M, F, or O"})
        if 'contact_info' in data and not data['contact_info']:
            raise serializers.ValidationError({"contact_info": "Contact info cannot be empty"})
        if 'medical_history' in data and not data['medical_history']:
            raise serializers.ValidationError({"medical_history": "Medical history cannot be empty"})
        return data
    
    def create(self, validated_data):
        try:
            name = validated_data.pop('name')
            
            # Create user
            name_parts = name.split()
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            username = name.lower().replace(' ', '_')
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                username = f"{username}_{User.objects.count()}"
            
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create patient
            patient = Patient.objects.create(
                user=user,
                **validated_data
            )
            return patient
            
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def update(self, instance, validated_data):
        try:
            # Update name if provided
            if 'name' in validated_data:
                name = validated_data.pop('name')
                name_parts = name.split()
                first_name = name_parts[0]
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                
                instance.user.first_name = first_name
                instance.user.last_name = last_name
                instance.user.save()
            
            # Update other fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            instance.save()
            return instance
            
        except Exception as e:
            raise serializers.ValidationError(str(e))

class AppointmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        required=True,
        source='patient'
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        required=True,
        source='doctor'
    )
    appointment_date = serializers.DateTimeField(
        required=True,
        source='appointment_time',
        format="%Y-%m-%dT%H:%M:%SZ",
        input_formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
    )
    status = serializers.ChoiceField(
        choices=['S', 'C', 'X'],
        required=True
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient_id', 'doctor_id', 'appointment_date', 'status', 'notes']
    
    def validate(self, data):
        if not data.get('patient'):
            raise serializers.ValidationError({"patient_id": "Patient ID is required"})
        if not data.get('doctor'):
            raise serializers.ValidationError({"doctor_id": "Doctor ID is required"})
        if not data.get('appointment_time'):
            raise serializers.ValidationError({"appointment_date": "Appointment date is required"})
        if not data.get('status'):
            raise serializers.ValidationError({"status": "Status is required"})
            
        # Check for existing appointment on the same date
        appointment_date = data['appointment_time'].date()
        existing_appointment = Appointment.objects.filter(
            patient=data['patient'],
            appointment_time__date=appointment_date,
            status='S'
        ).exists()
        
        if existing_appointment:
            raise serializers.ValidationError(
                {"appointment_date": "Patient already has an appointment scheduled for this date"}
            )
            
        return data
    
    def create(self, validated_data):
        try:
            appointment = Appointment.objects.create(**validated_data)
            return appointment
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def update(self, instance, validated_data):
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(str(e))

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'doctor', 'diagnosis',
            'prescriptions', 'lab_results', 'created_at', 'updated_at'
        ] 