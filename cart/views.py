from .models import Course, Cart
import requests
import json
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import CartItem, Cart, Payment, Enrollment


@login_required
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the course is already in the cart
    cart_item_exists = CartItem.objects.filter(
        cart=cart, course=course).exists()

    if not cart_item_exists:
        CartItem.objects.create(cart=cart, course=course)

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'items': cart.items.all(),
    }
    return render(request, 'cart/view_cart.html', context)


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


# payment form
def payement_form(request, cartItem_id):
    # getting specific cartItem
    cartItem = get_object_or_404(CartItem, id=cartItem_id)

    # getting course name
    course = cartItem.course

    # getting course price
    amount = cartItem.course.price

    # user associated with cartItem
    user = cartItem.cart.user

    context = {
        'cartItem': cartItem,
        'course': course,
        'amount': amount,
        'user': user,
    }

    return render(request, 'cart/payment_form.html', context=context)

# payment


@login_required
@csrf_exempt
def init_khalti(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = 'http://127.0.0.1:8000/cart/verify/'
    website_url = 'http://127.0.0.1:8000/cart/verify/'

    amount = int(cart_item.course.price) * 100
    transaction_id = str(uuid.uuid4())
    purchase_order_name = cart_item.course.course_title
    user = request.user
    email = user.email
    username = user.username
    phone = "9813000000"  # Replace with actual user phone number if available

    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount,
        "purchase_order_id": cart_item.id,
        "purchase_order_name": purchase_order_name,
        "transaction_id": transaction_id,
        "customer_info": {
            "name": username,
            "email": email,
            "phone": phone,
        },
        "product_details": [
            {
                "identity": cart_item.id,
                "name": purchase_order_name,
                "unit_price": amount,
                "total_price": amount,
                "quantity": 1
            }
        ],
        "merchant_username": username,
    })

    headers = {
        'Authorization': 'Key 4af23dc17ef244338b43239b43a3d8e1',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)
    new_res = response.json()

    if response.status_code == 200 and 'payment_url' in new_res:
        return redirect(new_res['payment_url'])
    else:
        return JsonResponse({'error': 'Failed to initiate payment', 'details': new_res}, status=400)


# what to do after payment
@csrf_exempt
def verify_khalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"

    if request.method == 'GET':
        headers = {
            'Authorization': f'Key 4af23dc17ef244338b43239b43a3d8e1',
            'Content-Type': 'application/json',
        }

        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        purchase_order_id = request.GET.get('purchase_order_id')

        if not all([pidx, transaction_id, purchase_order_id]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        data = json.dumps({'pidx': pidx})

        try:
            res = requests.post(url, headers=headers, data=data)
            res.raise_for_status()
            new_res = res.json()
        except requests.RequestException as e:
            return JsonResponse({'error': 'Request to Khalti failed', 'details': str(e)}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Failed to parse Khalti response'}, status=500)

        if new_res.get('status') == 'Completed':
            cart_item = get_object_or_404(CartItem, id=purchase_order_id)
            cart_item.is_paid = True
            cart_item.save()

            payment = Payment.objects.create(
                student=request.user,
                payment_id=transaction_id,
                # Convert from paisa to currency unit
                amount=new_res.get('total_amount', 0) / 100.0,
                paid_at=new_res.get('created_on', '2023-01-01T00:00:00Z'),
                course=cart_item.course,
                payment_status=new_res['status'],
            )

            Enrollment.objects.create(
                payment=payment,
                course=cart_item.course,
                is_enroll=True
            )

            return redirect('home')
        else:
            return JsonResponse({'error': 'Payment verification failed', 'details': new_res}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
