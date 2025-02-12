from App_1.models import *
from scry.RaceStatics.raceid_search import *

search=SearchID(2024)

search.create_query_set()

race_id=202406010101

obj=RaceHTML.objects.get(race_id=race_id)
print(obj)

search.save_race_html_to_file(race_id)