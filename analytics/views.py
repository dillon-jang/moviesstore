from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render

@staff_member_required
def top_commenters(request):
    users = list(
        User.objects
            .annotate(comment_count=Count('review'))
            .filter(comment_count__gt=0)
            .order_by('-comment_count', 'username')
    )

    template_data = {}
    template_data['title'] = 'User Engagement'
    template_data['users'] = users
    template_data['top_user'] = users[0] if users else None

    return render(request, 'analytics/top_commenters.html',
                    {'template_data': template_data})