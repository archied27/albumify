# albumify spec
Status: in development
## Goals
- To effectively organise, view and sort Spotify saved albums
    - encourage listening via albums not songs
- Through a React frontend
- Using ML techniques
## Checklist
- [x] Get users saved albums via oAuth
- [x] Add caching for artist fetches (many artists across library)
- [x] Get relevant data needed for ML
    - [x] spotify: album release year, artist(s) genre, average track duration
    - [x] last.fm: artist tags, album tags, 
- [x] Derive new features
    - [x] era encoding i.e 70s, 80s, etc
- [x] Create a clustering model to cluster together albums
- [x] Add basic organisation and sorting features (year, etc)
- [x] Fully create a functional backend
- [x] Create the frontend
- [x] Add frontend renaming
- [ ] Add frontend page labels
- [ ] Add genre lists / tags
- [ ] Add order by's on all albums page
- [ ] Add random album in context
## Possible Extensions
- More ML algorithms? Choose an album from a text prompt?
- Random Album