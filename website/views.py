from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage, EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.staticfiles import finders
from email.mime.image import MIMEImage
import logging

from .models import Service, Project, Testimonial, ContactMessage

log = logging.getLogger(__name__)


def home(request):
    services = Service.objects.all()[:4]
    projects = Project.objects.all()[:6]
    testimonials = Testimonial.objects.all()
    return render(request, "index.html", {
        "services": services,
        "projects": projects,
        "testimonials": testimonials,
    })


def services_view(request):
    items = Service.objects.all()
    return render(request, "services.html", {"services": items})


def projects_view(request):
    category = request.GET.get("category")
    qs = Project.objects.all()
    if category:
        qs = qs.filter(category=category)
    categories = Project.objects.values_list("category", flat=True).distinct()
    return render(request, "projects.html", {
        "projects": qs,
        "categories": categories,
        "selected": category,
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project_detail.html", {"project": project})


def about(request):
    stats = {
        "years_experience": 10,
        "projects_completed": Project.objects.count(),
        "happy_clients": max(Testimonial.objects.count() * 5, 20),
    }
    return render(request, "about.html", {"stats": stats})


def contact(request):
    """
    GET  -> show contact page
    POST -> save message; email internal notice to info@; email confirmation to visitor (with CID logo).
    """
    if request.method == "POST":
        # (Optional) honeypot:
        if (request.POST.get("company") or "").strip():
            return render(request, "contact.html", {"sent": True, "email_sent": True})

        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        subject = (request.POST.get("subject") or "").strip() or "Work"
        body_raw = (request.POST.get("message") or "").strip()
        body = strip_tags(body_raw)

        # Save to DB (embedding subject)
        combined_message = f"Subject: {subject}\n\n{body}" if subject else body
        ContactMessage.objects.create(
            name=name, email=email, phone=phone, message=combined_message
        )

        # ------- 1) Internal notification to info@ -------
        to_addr = getattr(settings, "EMAIL_HOST_USER", "info@ctproz.com")
        from_addr = getattr(settings, "DEFAULT_FROM_EMAIL", to_addr)

        internal_text = "\n".join([
            "New contact form submission from CTProz.com", "",
            f"Name:   {name or '—'}",
            f"Email:  {email or '—'}",
            f"Phone:  {phone or '—'}",
            f"Subject: {subject}",
            "",
            "Message:",
            body or "(no message)",
        ])

        try:
            internal_msg = EmailMessage(
                subject=f"[CTProz] {subject}",
                body=internal_text,
                from_email=from_addr,
                to=[to_addr],
                reply_to=[f"{name} <{email}>"] if email else None,
            )
            internal_msg.send(fail_silently=False)
            email_sent = True
        except BadHeaderError:
            log.exception("Email bad header (internal notice)")
            email_sent = False
        except Exception:
            log.exception("SMTP send failed (internal notice)")
            email_sent = False

        # ------- 2) Confirmation email to the visitor (CID logo) -------
        if email:
            try:
                ctx = {
                    "name": name or "there",
                    "subject": subject,
                    "message": body,
                    "company": {
                        "name": "CTProz",
                        "tagline": "Handyman & Property Maintenance",
                        "phone": "(949) 875-0940",
                        "email": "info@ctproz.com",
                        "city": "Branford, CT",
                        "site": "https://ctproz.pro",
                    },
                }
                text_content = render_to_string("emails/confirmation.txt", ctx)
                html_content = render_to_string("emails/confirmation.html", ctx)

                conf = EmailMultiAlternatives(
                    subject="We received your request — CTProz",
                    body=text_content,
                    from_email=from_addr,
                    to=[email],
                    reply_to=[to_addr],
                )
                conf.attach_alternative(html_content, "text/html")

                # Embed logo.png as inline image with Content-ID
                logo_path = finders.find("img/logo.png")  # looks in staticfiles dirs
                if logo_path:
                    with open(logo_path, "rb") as f:
                        img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<ctproz-logo>")    # note the brackets
                    img.add_header("Content-Disposition", "inline", filename="logo.png")
                    # For inline images, ensure related subtype
                    conf.mixed_subtype = "related"
                    conf.attach(img)
                else:
                    log.warning("Logo not found at static/img/logo.png — skipping CID embed")

                conf.send(fail_silently=False)  # don't silence so we can debug if needed
            except BadHeaderError:
                log.exception("Email bad header (confirmation)")
            except Exception:
                log.exception("SMTP send failed (confirmation)")

        return render(request, "contact.html", {"sent": True, "email_sent": email_sent})

    return render(request, "contact.html")
