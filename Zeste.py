from datetime import datetime, timezone
from zoneinfo import ZoneInfo

hora = '2025-08-25 15:57:28'

date = datetime(year=2025, month=8, day=25, hour=15, tzinfo=timezone.utc)
convertido = date.astimezone(ZoneInfo('Europe/Lisbon'))
print(convertido)



