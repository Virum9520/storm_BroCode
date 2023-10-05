def handle_uploaded_file(f):  
    with open('users/static/users/images/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
    return chunk