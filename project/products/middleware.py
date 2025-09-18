import time 

class ProductMiddleware :
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response= self.get_response(request)
        duration = time.time() - start_time

        if request.path.startswith('/products') :
            print(f'[Product] request to {request.path} took {duration:.3f} seconds')

        return response



