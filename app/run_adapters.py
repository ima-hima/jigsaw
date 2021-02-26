import api.src.models as models
import api.src.db as db
import api.src.adapters as adapters
import psycopg2

class RequestAndBuild:
    def __init__(self):
        self.client = adapters.Client()
        self.builder = adapters.Builder()
        self.conn = db.conn
        self.cursor = db.cursor


    def run(self, search_params = {'ll': "40.7,-74", "query": "tacos"}):
        merchants = self.client.request_venues(search_params)
        venue_foursquare_ids = [venue['id'] for venue in venues]
        venue_objs = []
        for foursquare_id in venue_foursquare_ids:
            venue_details = self.client.request_venue(foursquare_id)
            venue_obj = self.builder.run(venue_details, self.conn, self.cursor)
            venue_objs.append(venue_obj)
        return venue_objs


