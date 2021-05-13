from ..app import app
from flask import request, url_for


@app.context_processor
def utility_processor():
    def faceted_url(uri, param_name=None, param_value=None, deleted=False, multi=None, page=None):
        multi = multi or {}
        args = request.args.to_dict(flat=False)

        if not param_name and page:
            return url_for(uri, page=page, **{key:val for key, val in args.items() if key != "page"})

        if deleted and param_name in args:
            if isinstance(args[param_name], list) and len(args[param_name]) > 1:
                args[param_name].pop(args[param_name].index(param_value))
            else:
                args.pop(param_name)
        elif not deleted:
            if param_name in args and isinstance(args[param_name], list):
                args[param_name].append(param_value)
            elif param_name in args and param_name in multi:
                args[param_name] = [args[param_name], param_value]
            else:
                args[param_name] = param_value
        return url_for(uri, **args)

    def paginate(resultsPage, howmany=5):
        current, total = resultsPage.pagenum, resultsPage.pagecount
        if total <= 3:
            return []
        pages =[
            pageNum
            for pageNum in range(max(2, current-howmany), min(total, current+howmany))
        ]
        if max(2, current-howmany) > 2:
            pages.insert(0, "...")
        if min(total, current+howmany) < total:
            pages.append("...")
        return pages
    return {
        "faceted_url": faceted_url,
        "paginate": paginate
    }
