from django.shortcuts import render
import wikipedia

# Create your views here.
languages = ['EN', 'DE', 'ES', 'FR', 'IT',
             'ZH', 'AR', 'PT', 'RU', 'JA']


def fetch_view(request):
    context = {'languages': languages}

    if request.method == 'POST':
        search_input = request.POST.get('search_input', '')
        selected_language = request.POST.get('language', '')

        # Select language
        wikipedia.set_lang(selected_language)

        # Fetch data using Wikipedia API
        try:
            page = wikipedia.page(search_input)
            country_name = page.title
            extract = page.summary
        except wikipedia.exceptions.PageError:
            country_name = search_input
            extract = None
        except wikipedia.exceptions.DisambiguationError as e:
            country_name = search_input
            extract = f"Multiple results found for '{search_input}'. Please specify your search."
      

        context.update({
            'search_input': search_input,
            'country_name': country_name,
            'extract': extract,
        })

        return render(request, 'fetcher/result.html', context)
    return render(request, 'fetcher/fetch.html', context)
