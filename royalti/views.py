from django.shortcuts import render

def get_royalti(request):
    context = {
        'songs' : [
            {
                'title' : 'Fortnight',
                'album' : 'The Tortured',
                'artist' : 'Taylor Swift',
                'songwriter' : 'Taylor Swift',
                'genre' : 'Pop',
                'duration' : '4:03',
                'plays' : '47.378.923',
                'downloads' : '378.222'
            },
            {
                'title' : 'Fortnight',
                'album' : 'The Tortured',
                'artist' : 'Taylor Swift',
                'songwriter' : 'Taylor Swift',
                'genre' : 'Pop',
                'duration' : '4:03',
                'plays' : '47.378.923',
                'downloads' : '378.222'
            },
            {
                'title' : 'Fortnight',
                'album' : 'The Tortured',
                'artist' : 'Taylor Swift',
                'songwriter' : 'Taylor Swift',
                'genre' : 'Pop',
                'duration' : '4:03',
                'plays' : '47.378.923',
                'downloads' : '378.222'
            },
            {
                'title' : 'Fortnight',
                'album' : 'The Tortured',
                'artist' : 'Taylor Swift',
                'songwriter' : 'Taylor Swift',
                'genre' : 'Pop',
                'duration' : '4:03',
                'plays' : '47.378.923',
                'downloads' : '378.222'
            },
            {
                'title' : 'Fortnight',
                'album' : 'The Tortured',
                'artist' : 'Taylor Swift',
                'songwriter' : 'Taylor Swift',
                'genre' : 'Pop',
                'duration' : '4:03',
                'plays' : '47.378.923',
                'downloads' : '378.222'
            },
            {
                'title' : 'Fortnight',
                'album' : 'The Tortured',
                'artist' : 'Taylor Swift',
                'songwriter' : 'Taylor Swift',
                'genre' : 'Pop',
                'duration' : '4:03',
                'plays' : '47.378.923',
                'downloads' : '378.222'
            },
        ]
    }

    return render(request, "royalti.html", context)