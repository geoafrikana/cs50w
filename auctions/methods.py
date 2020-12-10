def save_listing(listing_title, bid_start, image_url, listing_category, listing_description, username ):
    from .models import Listing, User
    myproduct= Listing(title=listing_title, description = listing_description, price=bid_start, image_url = image_url, category = listing_category, seller=username)
    myproduct.save()