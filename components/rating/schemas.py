from components.rating.models import BaseRating


class RatingCreateBody(BaseRating):
    post_id: int


class RatingDetailResponse(BaseRating):
    id: int


class RatingUpdateBody(BaseRating):
    pass
