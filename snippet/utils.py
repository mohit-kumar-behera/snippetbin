def find_datetime_delta(start, end):
  val = end.strftime("%b %d, %Y")
  show_type = None

  delta = end - start
  days_passed = delta.days
  seconds_passed = delta.seconds

  if days_passed == 0:
    if seconds_passed > 3600:
      """ hours ago """
      v = seconds_passed // 3600 # hours
      t = 'hour'
    elif seconds_passed >= 60 and seconds_passed <= 3600:
      """ minutes ago """
      v = (seconds_passed // 60) % 60  # minutes
      t = 'minute'
    else:
      """ seconds ago """
      v = seconds_passed # seconds
      t = 'second'
    val = v
    show_type = t
  elif days_passed > 0 and days_passed <= 30:
    """ days ago """
    val = days_passed # days
    show_type = 'day'
  elif days_passed > 30 and days_passed <= 120:
    """ months ago """
    val = days_passed // 30 # month
    show_type = 'month'
  
  return val, show_type