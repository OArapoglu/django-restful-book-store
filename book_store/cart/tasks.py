import logging
from celery import shared_task

from .models import CartItem


logger = logging.getLogger(__name__)


@shared_task
def release_book_from_cart(cart_item_id):
    """
    Task to remove a book from the cart based on the cart item ID.

    Args:
    cart_item_id (int): The ID of the cart item to be removed.
    """
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        logger.info(
            f"Cart item with ID {cart_item_id} successfully removed from the cart."
        )
    except CartItem.DoesNotExist:
        logger.warning(f"Cart item with ID {cart_item_id} does not exist.")
    except Exception as e:
        logger.error(
            f"An error occurred while removing cart item with ID {cart_item_id}: {e}"
        )
