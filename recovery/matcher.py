from .models import Match
from items.models import Item


class ItemMatcher:

    @staticmethod
    def calculate_score(lost_item, found_item):

        score = 0

        if lost_item.catagory_id == found_item.catagory_id:
            score += 30

        if lost_item.color.lower() == found_item.color.lower():
            score += 20

        if lost_item.brand.lower() == found_item.brand.lower():
            score += 15

        if lost_item.location.lower() == found_item.location.lower():
            score += 15

        lost_words = set(lost_item.description.lower().split())
        found_words = set(found_item.description.lower().split())

        if lost_words & found_words:
            score += 20

        return score

    @staticmethod
    def find_matches(item):

        if item.itemtype == 'LOST':
            opposite_type = 'FOUND'
            lost_item = item
        else:
            opposite_type = 'LOST'
            lost_item = None

        opposite_items = Item.objects.filter(
            itemtype=opposite_type,
            status='ACTIVE'
        )

        matches = []

        for other_item in opposite_items:

            if item.itemtype == 'LOST':
                found_item = other_item
            else:
                lost_item = other_item
                found_item = item

            score = ItemMatcher.calculate_score(
                lost_item, found_item
            )

            if score >= 40:

                match, created = Match.objects.get_or_create(
                    lost_item=lost_item,
                    found_item=found_item,
                    defaults={'match_score': score}
                )

                if not created:
                    match.match_score = score
                    match.save()

                matches.append(match)

        return matches