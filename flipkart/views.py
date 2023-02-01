from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render, redirect
from .models import Product,Category,ProductImage
from django.core.files.base import ContentFile
from .forms import ProductFilterForm

# Create your views here.

def scrape_product(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        
        # Checking if the product is already saved

        if Product.objects.filter(url=url).exists():
            product = Product.objects.filter(url=url).first()
        else:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # scraping the data using BeautifulSoup

            title = soup.find('span', {'class': 'B_NuCI'}).text
            if soup.find('div', {'class': '_1mXcCf RmoJUa'}):
                description = soup.find('div', {'class': '_1mXcCf RmoJUa'}).text
            else:
                description = ""   
            price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text
            rating = soup.find('div', {'class': '_3LWZlK'}).text
            if soup.find('a', {'class': '_1fGeJ5 _2UVyXR _31hAvz'}):
                size = soup.find('a', {'class': '_1fGeJ5 _2UVyXR _31hAvz'}).text
            else:
                size =""
            category = soup.find_all('a', {'class': '_2whKao'})[1].text
            class1_elements = soup.find_all('img',{'class':'_2r_T1I _396QI4'})
            class2_elements = soup.find_all('img',{'class':'q6DClP'})
            image_urls = []
            for element in class1_elements + class2_elements:
                image_url = element["src"]
                image_urls.append(image_url)
            

            # saving the scraped data to the model

            # Checking the category is already saved

            all_category = Category.objects.all()
            if all_category:
                for item in all_category:
                    if category != item.name:
                        category = Category(name=category)
                        category.save()
            else:            
                category = Category(name=category)
                category.save()
            all_category = Category.objects.filter(name=category) 
            category = all_category[0]   
            product = Product(
                url=url,
                title=title,
                description=description,
                price=price,
                rating=rating,
                size=size,
                category=category
            )
            product.save()
            for i, image in enumerate(image_urls):
                print(image)
                response = requests.get(image)
                product_image = ProductImage(product=product)
                product_image.image.save(f"image_{i}.jpg", ContentFile(response.content))
                product_image.save()
        return redirect('scraped_data',pk=product.pk)
    return render(request, 'index.html')


def scraped_data(request,pk):
    product = Product.objects.get(pk=pk)
    if product:
        images = ProductImage.objects.filter(product=product)
        return render(request, 'list.html', {'product': product,'images':images})
    else:
        return redirect('list_product')    

def list_products(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductFilterForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            if category:
                products = products.filter(category=category)
    else:
        form = ProductFilterForm()
    context = {
        'products': products,
        'form': form,
    }
    return render(request, 'index.html', context)   
