from .models import Match
from items.models import Item


class ItemMatcher:

    @staticmethod
    def calculate_location_score(lost_location, found_location):

        lost_parts = [
            part.strip().lower()
            for part in lost_location.split(' - ')
        ]

        found_parts = [
            part.strip().lower()
            for part in found_location.split(' - ')
        ]

        if len(lost_parts) != 3 or len(found_parts) != 3:
            return 0

        score = 0

        if lost_parts[0] == found_parts[0]:
            score += 5

        if lost_parts[1] == found_parts[1]:
            score += 8

        if lost_parts[2] == found_parts[2]:
            score += 12

        return score

    @staticmethod
    def calculate_score(lost_item, found_item):

        score = 0

        if lost_item.catagory_id == found_item.catagory_id:
            score += 20

        if lost_item.color.strip().lower() == found_item.color.strip().lower():
            score += 25

        if lost_item.brand.strip().lower() == found_item.brand.strip().lower():
            score += 30

        score += ItemMatcher.calculate_location_score(
            lost_item.location,
            found_item.location
        )

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
                lost_item,
                found_item
            )

            existing_match = Match.objects.filter(
                lost_item=lost_item,
                found_item=found_item
            ).first()

            if score > 75:

                match, created = Match.objects.get_or_create(
                    lost_item=lost_item,
                    found_item=found_item,
                    defaults={
                        'match_score': score,
                        'status': 'PENDING'
                    }
                )

                if not created:
                    match.match_score = score
                    match.save(update_fields=['match_score'])

                matches.append(match)

            elif existing_match:
                existing_match.delete()

        return matches
