from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from .models import Result

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        test_score = cleaned_data.get('test_score')
        exam_score = cleaned_data.get('exam_score')
        
        if test_score is not None and exam_score is not None:
            # Convert float multipliers to Decimal for proper calculation
            test_weight = Decimal('0.3')
            exam_weight = Decimal('0.7')
            
            # Calculate total score using Decimal arithmetic
            total_score = (test_score * test_weight) + (exam_score * exam_weight)
            cleaned_data['total_score'] = total_score
            
            # Determine grade
            if total_score >= Decimal('80'):
                cleaned_data['grade'] = 'A'
            elif total_score >= Decimal('70'):
                cleaned_data['grade'] = 'B'
            elif total_score >= Decimal('60'):
                cleaned_data['grade'] = 'C'
            elif total_score >= Decimal('50'):
                cleaned_data['grade'] = 'D'
            else:
                cleaned_data['grade'] = 'F'
        
        return cleaned_data