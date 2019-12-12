from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404

import copy
import json

from premium.utils import is_premium
from .utils import page_utils, collection_utils
from .forms import AddNewPageForm, EditPageForm
from .models import Bookmark, Collection, Page
# from .utils import change_num_columns


# Create your views here.
def links(request, page):
    # check page exists, redirect if not
    try:
        page = Page.objects.get(user=request.user, name=page)
    except ObjectDoesNotExist:
        return redirect('links', page='qhome')  # qhome currently, to see errs

    bookmarks = Bookmark.objects.filter(
        user__username=request.user
        )
    collections = Collection.objects.filter(
        user__username=request.user).filter(
        page__name=page.name
        ).order_by('position')

    # page forms
    add_new_page_form = AddNewPageForm(
        current_user=request.user
    )

    edit_page_form = EditPageForm(
        current_user=request.user
    )

    # add new page form
    if 'add-page-form' in request.POST:
        form_data = AddNewPageForm(request.POST, current_user=request.user)
        if form_data.is_valid():
            new_page = page_utils.add_page(request, form_data)
            return redirect('links', page=new_page)

        else:
            add_new_page_form = form_data

    # edit page form
    if 'edit-page-form' in request.POST:
        form_data = EditPageForm(request.POST, current_user=request.user)
        if form_data.is_valid():
            new_page_name = form_data.cleaned_data.get('name')
            name = page_utils.edit_page_name(request, new_page_name, page)
            return redirect('links', page=name)

        else:
            edit_page_form = form_data

    # delete page form
    if 'delete-page-form' in request.POST:
        page_utils.delete_page(request, page)
        return redirect('links', page='home')

    # add a new collection
    if 'add-collection' in request.POST:
        # check name is allowed
        if collection_utils.validate_name(request, collections, page):
            # add collection name to db
            collection_utils.add_collection(request, page)

        return redirect('links', page=page)

    # delete collection
    if 'delete-collection-form' in request.POST:

        collection_to_delete = get_object_or_404(
            Collection,
            page__name=page.name,
            user=request.user,
            name=request.POST.get('collection')
        )
        position_to_delete = collection_to_delete.position
        collection_to_delete.delete()
        messages.success(
                request, f"Collection Deletion Successful")

        # reset collection.position for each
        for count, collection in enumerate((collections), 1):
            # print(collection, " ", count)
            collection.position = count
            collection.save()

        # reset column ordering numbers for each 2 through 5
        new_collection_orders = []
        for i in range(2, 6):
            collection_order = json.loads(
                eval('page.collection_order_'+str(i)))

            # find deleted position and remove from list
            for x in collection_order:
                if position_to_delete in x:
                    x.remove(position_to_delete)

            # rename remaining positions starting from 1
            count = 1
            for col in range(len(collection_order)):
                for pos in range(len(collection_order[col])):
                    # if collection_order[col][pos]:
                    collection_order[col][pos] = count
                    # print(collection_order[col][pos])
                    count += 1

            new_collection_orders.append(collection_order)

        page.collection_order_2 = new_collection_orders[0]
        page.collection_order_3 = new_collection_orders[1]
        page.collection_order_4 = new_collection_orders[2]
        page.collection_order_5 = new_collection_orders[3]
        page.save()

        return redirect('links', page=page)

    # create list of page names for sidebar
    all_page_names = []
    all_pages = Page.objects.filter(user=request.user)
    for name in all_pages:
        all_page_names.append(name.name)

    # generate collection names & order
    num_of_columns = page.num_of_columns
    if num_of_columns != 1:
        # get the display order for the collections from the db
        collection_order = json.loads(
            eval('page.collection_order_'+str(page.num_of_columns)))
        collection_list = copy.deepcopy(collection_order)

        # put collection names into a list. add them in order based on
        # the value of collection.position and map this to the structure
        # of collection_list

        count = 0
        for col in range(num_of_columns):
            if collection_list[col] != []:
                for pos in range(len(collection_list[col])):
                    count += 1
                    collection_name = get_object_or_404(
                        Collection,
                        page__name=page.name,
                        user=request.user,
                        position=count
                    )
                    collection_list[col][pos] = str(collection_name)
    else:
        # single columm collection display
        collection_list = [[]]
        if collections.count() > 0:
            for i in range(collections.count()):
                collection_name = get_object_or_404(
                    Collection,
                    page__name=page.name,
                    user=request.user,
                    position=i+1
                )
                collection_list[0].append(str(collection_name))

    # iterate through collection names and create a qs of bookmarks for each
    bm_data = []
    for x in range(num_of_columns):
        column = {}
        for j in (collection_list[x]):
            qs = bookmarks.filter(collection__name=j).order_by('position')
            column[j] = qs
        bm_data.append(column)

    # set this page as the last page visited
    request.session['last_page'] = page.name

    # testing....

    context = {"column_width": 100 / num_of_columns,
               "num_of_columns": num_of_columns,
               "bm_data": bm_data,
               "page": page.name,
               "all_page_names": all_page_names,
               "add_new_page_form": add_new_page_form,
               "edit_page_form": edit_page_form, }
    context = is_premium(request.user, context)

    return render(request, 'links/links.html', context)
