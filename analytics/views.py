from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from movies.models import Movie

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

@staff_member_required
def movie_stats(request):
    most_bought = None
    most_reviewed = None
    most_bought_count = 0
    most_reviewed_count = 0

    for movie in Movie.objects.all():
        bought = 0
        for item in movie.item_set.all():
            bought += item.quantity
        if bought > most_bought_count:
            most_bought_count = bought
            most_bought = movie

        reviewed = movie.review_set.count()
        if reviewed > most_reviewed_count:
            most_reviewed_count = reviewed
            most_reviewed = movie
    template_data = {}
    template_data['title'] = 'Movie Stats'
    template_data['most_bought'] = most_bought
    template_data['most_bought_count'] = most_bought_count
    template_data['most_reviewed'] = most_reviewed
    template_data['most_reviewed_count'] = most_reviewed_count

    return render(request, 'analytics/movie_stats.html', {'template_data': template_data})
