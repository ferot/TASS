# TASS
Application showing most popular tracks by user's opinion from two travel forums.

#Installation: 
$cd utils
$sudo ./prep_env.sh

#Runnning:

1. If full-proccess is desired (with webscraping posts from forum's) please run:
$python main_app ws
where ws is input param

2. When main_app finishes processing:
$python3 -m http.server

3.Open any webbrowser, and proceed to http://localhost:8000/trasy.html
