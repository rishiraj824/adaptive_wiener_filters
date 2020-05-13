from django.http import JsonResponse
from .models import *
from .WienerFilter import *
import os
from django.views.decorators.csrf import csrf_exempt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        data = request.POST.copy()
        image = request.FILES.get('image')

        name = data.get('name')

        color = data.get('color')
        type(color)

        Images.objects.create(name=name, image=image)

        if color:
            image = loadImage(os.path.join(BASE_DIR, 'media/images/') + name, 1)
            wiener = WienerFilter(image, (11, 11))
            output = wiener.estimateOutputColorised()
        else:
            image = loadImage(os.path.join(BASE_DIR, 'media/images/') + name, 0)
            wiener = WienerFilter(image, (5, 5))
            output = wiener.estimateOutput()

        # sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # sharpen = cv.filter2D(output, -1, sharpen_kernel)
        # print(sharpen)
        cv.imwrite(os.path.join(BASE_DIR, 'media/images/') + 'processed_' + name, output)

        return JsonResponse(
            {"message": "Image Succesfully Processed", "image": 'http://127.0.0.1:8000/media/images/' + 'processed_' + name},
            status=200)



    if request.method == 'GET':
        return JsonResponse({"message": "Nothing to return"}, status=200)
