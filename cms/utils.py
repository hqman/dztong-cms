def get_pagenum(request):
    '''Get the page number form GET query, default is page 1'''
    page = request.GET.get('page', '')
    if not page:
        page = 1
    return page