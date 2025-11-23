from datetime import datetime, timedelta, time
from typing import List, Dict, Optional
from django.utils import timezone
from .models import Doctor, Appointment


def get_doctor_schedule(doctor: Doctor, date: datetime.date) -> Optional[Dict[str, time]]:
    """
    Get doctor's working hours for a specific date.
    
    Args:
        doctor: Doctor instance
        date: Date to check schedule for
        
    Returns:
        Dictionary with start_time, end_time, break_start, break_end
        Returns None if doctor doesn't work on that day
    """
    day_name = date.strftime('%A').lower()
    schedule = doctor.schedule.get(day_name, {})
    
    if not schedule:
        # Default schedule if not specified
        return {
            'start_time': time(9, 0),
            'end_time': time(17, 0),
            'break_start': time(12, 0),
            'break_end': time(13, 0),
        }
    
    # Parse time strings from schedule
    try:
        return {
            'start_time': datetime.strptime(schedule.get('start', '09:00'), '%H:%M').time(),
            'end_time': datetime.strptime(schedule.get('end', '17:00'), '%H:%M').time(),
            'break_start': datetime.strptime(schedule.get('break_start', '12:00'), '%H:%M').time() if 'break_start' in schedule else None,
            'break_end': datetime.strptime(schedule.get('break_end', '13:00'), '%H:%M').time() if 'break_end' in schedule else None,
        }
    except (ValueError, KeyError):
        # Fallback to default if parsing fails
        return {
            'start_time': time(9, 0),
            'end_time': time(17, 0),
            'break_start': time(12, 0),
            'break_end': time(13, 0),
        }


def get_available_slots(doctor: Doctor, date: datetime.date, duration: int = 30) -> List[datetime]:
    """
    Calculate available time slots for a doctor on a given date.
    
    Args:
        doctor: Doctor instance
        date: Date to check availability for
        duration: Appointment duration in minutes (default 30)
        
    Returns:
        List of available datetime slots
    """
    schedule = get_doctor_schedule(doctor, date)
    if not schedule:
        return []
    
    # Get all existing appointments for this doctor on this date
    start_of_day = timezone.make_aware(datetime.combine(date, time.min))
    end_of_day = timezone.make_aware(datetime.combine(date, time.max))
    
    existing_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_time__gte=start_of_day,
        appointment_time__lte=end_of_day,
        status='S'  # Only consider scheduled appointments
    )
    
    # Create a set of booked time ranges
    booked_slots = set()
    for appointment in existing_appointments:
        slot_start = appointment.appointment_time
        slot_end = slot_start + timedelta(minutes=appointment.duration)
        
        # Mark all minutes in this range as booked
        current = slot_start
        while current < slot_end:
            booked_slots.add(current.replace(second=0, microsecond=0))
            current += timedelta(minutes=1)
    
    # Generate all possible slots
    available_slots = []
    current_time = timezone.make_aware(datetime.combine(date, schedule['start_time']))
    end_time = timezone.make_aware(datetime.combine(date, schedule['end_time']))
    
    # Handle break times
    break_start = None
    break_end = None
    if schedule.get('break_start') and schedule.get('break_end'):
        break_start = timezone.make_aware(datetime.combine(date, schedule['break_start']))
        break_end = timezone.make_aware(datetime.combine(date, schedule['break_end']))
    
    while current_time + timedelta(minutes=duration) <= end_time:
        slot_end = current_time + timedelta(minutes=duration)
        
        # Check if slot is during break time
        is_during_break = False
        if break_start and break_end:
            if not (slot_end <= break_start or current_time >= break_end):
                is_during_break = True
        
        # Check if any minute in this slot is booked
        is_booked = False
        check_time = current_time
        while check_time < slot_end:
            if check_time in booked_slots:
                is_booked = True
                break
            check_time += timedelta(minutes=1)
        
        # Only add if not booked and not during break
        if not is_booked and not is_during_break and current_time > timezone.now():
            available_slots.append(current_time)
        
        # Move to next slot
        current_time += timedelta(minutes=duration)
    
    return available_slots


def is_slot_available(doctor: Doctor, start_time: datetime, duration: int = 30) -> bool:
    """
    Check if a specific time slot is available for a doctor.
    
    Args:
        doctor: Doctor instance
        start_time: Proposed appointment start time
        duration: Appointment duration in minutes (default 30)
        
    Returns:
        True if slot is available, False otherwise
    """
    # Check if in the past
    if start_time <= timezone.now():
        return False
    
    # Get doctor's schedule for this day
    schedule = get_doctor_schedule(doctor, start_time.date())
    if not schedule:
        return False
    
    # Check if within working hours
    appointment_time = start_time.time()
    if appointment_time < schedule['start_time'] or appointment_time >= schedule['end_time']:
        return False
    
    # Check if during break time
    if schedule.get('break_start') and schedule.get('break_end'):
        break_start = schedule['break_start']
        break_end = schedule['break_end']
        slot_end = (start_time + timedelta(minutes=duration)).time()
        
        # Slot overlaps with break if it doesn't end before break starts or start after break ends
        if not (slot_end <= break_start or appointment_time >= break_end):
            return False
    
    # Check for conflicting appointments
    slot_end = start_time + timedelta(minutes=duration)
    
    conflicting_appointments = Appointment.objects.filter(
        doctor=doctor,
        status='S',
        appointment_time__lt=slot_end,
        appointment_time__gte=start_time - timedelta(minutes=60)  # Check nearby appointments
    )
    
    for appointment in conflicting_appointments:
        existing_end = appointment.appointment_time + timedelta(minutes=appointment.duration)
        
        # Check if there's any overlap
        if not (slot_end <= appointment.appointment_time or start_time >= existing_end):
            return False
    
    
    return True
