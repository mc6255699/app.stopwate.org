# invoices/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvoiceForm
from .models import Invoice
from core.pdfutils import generate_cover_page, merge_cover_with_invoice
from django.core.files.base import ContentFile


@login_required
def upload_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.owner = request.user
            invoice.save()

            # ✅ Generate stamped PDF
            cover_pdf = generate_cover_page(invoice)
            merged_pdf = merge_cover_with_invoice(cover_pdf, invoice.uploaded_pdf)

            invoice.stamped_pdf.save(
                f"{invoice.code}_stamped.pdf",
                ContentFile(merged_pdf.read()),
                save=True
            )

            return render(request, 'invoices/upload.html', {
                'form': InvoiceForm(),  # reset the form
                'success': True,
                'uploaded_pdf_url': invoice.stamped_pdf.url  # ✅ pass URL for preview
            })
    else:
        form = InvoiceForm()

    return render(request, 'invoices/upload.html', {'form': form})

#def invoice_detail(request, pk=None):
#    invoice = get_object_or_404(Invoice, pk=pk)
#    return render(request, 'invoices/detail.html', {'invoice': invoice})

def search_invoice(request):
    return render(request, 'invoices/search.html')  # Placeholder for search functionality
