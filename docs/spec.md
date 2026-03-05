# albumify spec
Status: in development
## Goals
- To effectively organise, view and sort Spotify shared albums
- Through a React frontend
- Using ML techniques
## Checklist
- [ ] Get users saved albums via oAuth
- [ ] Get relevant data needed for ML
    - spotify: album release year, artist(s) genre, average track duration
    - last.fm: artist tags, album tags, 
- [ ] Derive new features
    - genre embedding
    - era encoding i.e 70s, 80s, etc
- [ ] Create a clustering model to cluster together albums
- [ ] Add basic organisation and sorting features (year, etc)
- [ ] Fully create a functional backend
- [ ] Create the frontend
## Possible Extensions
- More ML algorithms? Choose an album from a text prompt?