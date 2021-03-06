from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from links.utils import bookmark_utils
from premium.utils import is_premium

from links.models import Page, Bookmark
from links.utils.general_utils import set_page_name


@login_required
def search(request):

    # if user is deleting a bookmark from search results
    if 'delete-bookmark-form' in request.POST:
        bookmark_utils.delete_bookmark(request)

    # Fetch form search query
    q = request.GET.get('q')
    q = "" if q is None else q

    results_per_page = 10

    # find bookmarks based on search query
    search_qs = Bookmark.objects.filter(
        user=request.user, title__icontains=q
    ).order_by('added')

    # pagination
    results_page = request.GET.get('rpage', 1)

    paginator = Paginator(search_qs, results_per_page)
    try:
        search_results = paginator.page(results_page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    # get pages for sidebar
    all_pages = Page.objects.filter(user=request.user).order_by('position')

    # set page value for default page choice for 'add bookmark' button
    page = set_page_name(request)

    # bookmark paramaters for use with the 'delete_modal' template
    bm_delete_modal = {"form_name": "delete-bookmark-form",
                       "object_type": "bookmark",
                       "text": "the bookmark will be permanently deleted.", }

    context = {
        "all_page_names": all_pages,
        "page": page,
        "q": q,
        "search_results": search_results,
        "p": paginator,
        "page_num": results_page,
        "bm_delete_modal": bm_delete_modal,
    }
    context = is_premium(request.user, context)

    return render(request, 'search/search_results.html', context)
