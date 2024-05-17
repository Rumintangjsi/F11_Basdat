# def get_podcast(email_podcaster)
    # query = f"SELECT * FROM podcast WHERE email_podcaster = '{email_podcaster}';"
    #return query

def get_podcast():
    return "SELECT * FROM podcast WHERE email_podcaster = 'alexpage@example.org';"


def get_konten(id_konten):
    return f"SELECT * FROM konten WHERE id = '{id_konten}';"