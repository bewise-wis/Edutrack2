# reports/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.base import ContentFile
import os
import tempfile
import logging

logger = logging.getLogger(__name__)

# Try to import WeasyPrint with fallback
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    logger.warning("WeasyPrint is not installed. PDF generation will not work.")

from .models import Report, StudentReport, ClassReport
from students.models import Student
from classes.models import Class
from results.models import Result
from django.db.models import Avg, Count

# Add the missing report_list function
@login_required
def report_list(request):
    reports = Report.objects.filter(generated_by=request.user).order_by('-generated_at')
    return render(request, 'reports/report_list.html', {'reports': reports})

@login_required
def generate_student_report(request):
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student')
            semester = request.POST.get('semester')
            
            if not student_id or not semester:
                messages.error(request, 'Please select both student and semester.')
                return redirect('generate_student_report')
            
            student = get_object_or_404(Student, id=student_id)
            results = Result.objects.filter(student=student, semester=semester)
            
            if not results.exists():
                messages.error(request, 'No results found for this student in the selected semester.')
                return redirect('generate_student_report')
            
            # Calculate statistics
            overall_average = results.aggregate(avg=Avg('total_score'))['avg'] or 0
            total_subjects = results.count()
            
            # Create report record first
            report = Report.objects.create(
                report_type='student',
                title=f"Student Report - {student.user.get_full_name()} - Semester {semester}",
                generated_by=request.user,
                parameters={'student_id': student_id, 'semester': semester}
            )
            
            StudentReport.objects.create(
                report=report,
                student=student,
                overall_average=overall_average,
                total_subjects=total_subjects
            )
            
            # Only generate PDF if WeasyPrint is available
            if WEASYPRINT_AVAILABLE:
                try:
                    # Generate HTML content
                    html_string = render_to_string('reports/student_report_pdf.html', {
                        'student': student,
                        'results': results,
                        'overall_average': overall_average,
                        'semester': semester,
                    })
                    
                    # Create PDF
                    html = HTML(string=html_string)
                    pdf_data = html.write_pdf()
                    
                    # Save PDF to file
                    filename = f'student_report_{student_id}_{semester}.pdf'
                    report.file.save(filename, ContentFile(pdf_data))
                    
                    messages.success(request, 'Student report generated successfully with PDF!')
                except Exception as e:
                    logger.error(f"PDF generation failed: {e}")
                    messages.warning(request, 'Report created but PDF generation failed. Please check server logs.')
            else:
                messages.success(request, 'Student report generated successfully! (PDF generation disabled)')
            
            return redirect('report_list')
            
        except Exception as e:
            logger.error(f"Error generating student report: {e}")
            messages.error(request, f'Error generating report: {str(e)}')
            return redirect('generate_student_report')
    
    students = Student.objects.all()
    return render(request, 'reports/generate_student_report.html', {
        'students': students,
        'weasyprint_available': WEASYPRINT_AVAILABLE
    })

@login_required
def generate_class_report(request):
    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            semester = request.POST.get('semester')
            
            class_obj = get_object_or_404(Class, id=class_id)
            students = Student.objects.filter(current_class=class_obj)
            
            if not students.exists():
                messages.error(request, 'No students found in this class.')
                return redirect('generate_class_report')
            
            # Calculate class statistics
            class_results = Result.objects.filter(
                student__current_class=class_obj,
                semester=semester
            )
            
            class_average = class_results.aggregate(avg=Avg('total_score'))['avg'] or 0
            total_students = students.count()
            
            # Calculate pass rate (assuming 50 is passing)
            passed_students = class_results.filter(total_score__gte=50).values('student').distinct().count()
            pass_rate = (passed_students / total_students * 100) if total_students > 0 else 0
            
            # Create report record
            report = Report.objects.create(
                report_type='class',
                title=f"Class Report - {class_obj.name} - Semester {semester}",
                generated_by=request.user,
                parameters={'class_id': class_id, 'semester': semester}
            )
            
            ClassReport.objects.create(
                report=report,
                class_obj=class_obj,
                class_average=class_average,
                total_students=total_students,
                pass_rate=pass_rate
            )
            
            messages.success(request, 'Class report generated successfully!')
            return redirect('report_list')
            
        except Exception as e:
            logger.error(f"Error generating class report: {e}")
            messages.error(request, 'Error generating class report. Please try again.')
            return redirect('generate_class_report')
    
    classes = Class.objects.all()
    return render(request, 'reports/generate_class_report.html', {'classes': classes})

@login_required
def view_report(request, report_id):
    report = get_object_or_404(Report, id=report_id, generated_by=request.user)
    
    if report.file:
        response = HttpResponse(report.file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{report.title}.pdf"'
        return response
    
    messages.error(request, 'Report file not found.')
    return redirect('report_list')

@login_required
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id, generated_by=request.user)
    
    if request.method == 'POST':
        if report.file:
            report.file.delete()
        report.delete()
        messages.success(request, 'Report deleted successfully!')
        return redirect('report_list')
    
    return render(request, 'reports/confirm_delete.html', {'report': report})