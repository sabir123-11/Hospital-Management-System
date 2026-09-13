import json
import re
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST

from .models import Appointment, ContactMessage, CareerApplication, PatientProfile, ChatLog


# ---------- Static page views (serve existing HTML unchanged) ----------

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def departments(request):
    return render(request, 'departments.html')

def doctors(request):
    return render(request, 'doctors.html')

def services(request):
    return render(request, 'services.html')

def gallery(request):
    return render(request, 'gallery.html')

def blog(request):
    return render(request, 'blog.html')

def faq(request):
    return render(request, 'faq.html')

def careers(request):
    return render(request, 'careers.html')

def contact(request):
    return render(request, 'contact.html')

def appointment(request):
    return render(request, 'appointment.html')

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def privacy(request):
    return render(request, 'privacy-policy.html')

def terms(request):
    return render(request, 'terms.html')


# ---------- Form submission endpoints ----------

@csrf_exempt
@require_POST
def submit_appointment(request):
    try:
        data = request.POST
        appt = Appointment.objects.create(
            full_name=data.get('full_name', '').strip(),
            phone=data.get('phone', '').strip(),
            email=data.get('email', '').strip(),
            department=data.get('department', '').strip(),
            preferred_date=data.get('preferred_date') or None,
            preferred_time=data.get('preferred_time') or None,
            reason=data.get('reason', '').strip(),
        )
        return JsonResponse({'success': True, 'message': 'Appointment booked successfully!', 'id': appt.id})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_POST
def submit_contact(request):
    try:
        data = request.POST
        msg = ContactMessage.objects.create(
            name=data.get('name', '').strip(),
            email=data.get('email', '').strip(),
            subject=data.get('subject', '').strip(),
            message=data.get('message', '').strip(),
        )
        return JsonResponse({'success': True, 'message': 'Message sent successfully!', 'id': msg.id})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_POST
def submit_career(request):
    try:
        data = request.POST
        app = CareerApplication.objects.create(
            full_name=data.get('full_name', '').strip(),
            email=data.get('email', '').strip(),
            position=data.get('position', '').strip(),
            years_experience=data.get('years_experience', '').strip(),
            resume_notes=data.get('resume_notes', '').strip(),
        )
        return JsonResponse({'success': True, 'message': 'Application submitted successfully!', 'id': app.id})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_POST
def submit_register(request):
    try:
        data = request.POST
        first = data.get('first_name', '').strip()
        last = data.get('last_name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        phone = data.get('phone', '').strip()
        dob = data.get('date_of_birth') or None
        gender = data.get('gender', '').strip()

        if User.objects.filter(username=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already registered.'}, status=400)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first,
            last_name=last,
        )
        PatientProfile.objects.create(
            user=user,
            phone=phone,
            date_of_birth=dob,
            gender=gender,
        )
        login(request, user)
        return JsonResponse({'success': True, 'message': 'Account created successfully!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_POST
def submit_login(request):
    try:
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Logged in successfully!'})
        return JsonResponse({'success': False, 'message': 'Invalid email or password.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def submit_logout(request):
    logout(request)
    return redirect('index')


# ---------- Chatbot ----------

CHATBOT_KB = [
    {
        'keywords': ['hello', 'hi', 'hey', 'good morning', 'good evening', 'namaste'],
        'response': 'Hello! Welcome to City Care Hospital. How can I help you today? You can ask about appointments, departments, doctors, emergency, visiting hours, or insurance.',
    },
    {
        'keywords': ['appointment', 'book', 'schedule', 'consult'],
        'response': 'You can book an appointment online on our Appointment page, call +91 12345 67890, or walk in during OPD hours (Mon–Sat 8 AM–9 PM). Visit /appointment to book now.',
    },
    {
        'keywords': ['emergency', 'ambulance', 'trauma', 'urgent'],
        'response': 'Our Emergency & Trauma Centre is open 24×7. Call +91 12345 67890 immediately. GPS-tracked ambulances with paramedic support are available.',
    },
    {
        'keywords': ['department', 'specialt', 'cardiology', 'neurology', 'pediatric', 'orthopedic', 'radiology'],
        'response': 'We have 18 specialty departments including Cardiology, Neurology, Pediatrics, Orthopedics, Radiology, Emergency and more. See the Departments page for details.',
    },
    {
        'keywords': ['doctor', 'specialist', 'physician'],
        'response': 'We have 120+ specialists. Visit the Doctors page to meet our team including Dr. Ananya Sharma (Cardiologist), Dr. Rohan Mehta (Neurologist), Dr. Priya Nair (Pediatrician) and others.',
    },
    {
        'keywords': ['hours', 'timing', 'open', 'opd', 'visiting'],
        'response': 'OPD hours: Monday–Saturday, 8:00 AM – 9:00 PM. Emergency services are available 24×7 every day of the year.',
    },
    {
        'keywords': ['location', 'address', 'where', 'direction', 'cuttack'],
        'response': 'City Care Hospital is at 12 Wellness Avenue, Cuttack, Odisha 753001. You can find directions from the Contact page.',
    },
    {
        'keywords': ['phone', 'call', 'contact', 'number'],
        'response': 'Main number / Emergency: +91 12345 67890. Email: care@citycarehospital.in. Appointments: appointments@citycarehospital.in.',
    },
    {
        'keywords': ['insurance', 'cashless', 'policy'],
        'response': 'Yes, we offer cashless treatment with most major insurance providers. Please bring your policy card and photo ID at admission.',
    },
    {
        'keywords': ['report', 'lab', 'test', 'result'],
        'response': 'Registered patients can download lab reports from the Patient Login portal as soon as they are ready. Our NABL-accredited lab provides same-day reporting for many tests.',
    },
    {
        'keywords': ['icu', 'intensive', 'critical'],
        'response': 'We have a Level-3 ICU with continuous monitoring and a dedicated critical-care team. Nurse-to-patient ratio is maintained at 1:2.',
    },
    {
        'keywords': ['pharmacy', 'medicine', 'medication'],
        'response': 'Our in-house pharmacy is open 24×7 and stocks genuine medication. Home delivery is available for discharged patients.',
    },
    {
        'keywords': ['career', 'job', 'vacancy', 'opening', 'apply'],
        'response': 'Current openings are listed on the Careers page. You can apply online there or email your resume to care@citycarehospital.in.',
    },
    {
        'keywords': ['nabh', 'accreditation', 'quality'],
        'response': 'City Care Hospital is NABH accredited and ISO 9001:2015 certified. We follow strict quality and infection-control protocols.',
    },
    {
        'keywords': ['thank', 'thanks', 'bye', 'goodbye'],
        'response': 'You are welcome! Take care. If you need anything else, just ask. For emergencies call +91 12345 67890.',
    },
]


def get_chatbot_response(message: str) -> str:
    msg = message.lower().strip()
    if not msg:
        return 'Please type a question. I can help with appointments, departments, emergency, doctors, hours and more.'

    for item in CHATBOT_KB:
        for kw in item['keywords']:
            if kw in msg:
                return item['response']

    return (
        "I'm not sure about that. You can ask me about:\n"
        "• Booking appointments\n"
        "• Departments & doctors\n"
        "• Emergency / ambulance\n"
        "• Visiting hours & location\n"
        "• Insurance & lab reports\n"
        "Or call +91 12345 67890 for immediate help."
    )


@csrf_exempt
@require_http_methods(['POST'])
def chatbot_api(request):
    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
        user_msg = (body.get('message') or '').strip()
        session_id = body.get('session_id', '')[:64]
        reply = get_chatbot_response(user_msg)
        ChatLog.objects.create(
            session_id=session_id,
            user_message=user_msg,
            bot_response=reply,
        )
        return JsonResponse({'success': True, 'reply': reply})
    except Exception as e:
        return JsonResponse({'success': False, 'reply': 'Sorry, something went wrong. Please try again or call +91 12345 67890.'}, status=500)
