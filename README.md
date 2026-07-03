# albumify
Organise Spotify saved albums using HDBSCAN and lastfm's API

## Motivation
I was motivated to make this due to Spotify's lack of features surrounding albums, and I believe listening to music via albums should be encouraged and a lot of the art of music is lost listening through playlists instead of albums

And my personal library consists of ~1000 saved albums, which can be difficult to browse with Spotify's limited sorting (by artist name, album name, year, recently added), so this project will also be useful for myself

---

## Demo
![demo](/docs/demo.gif)

## Features
This fetches a users spotify albums using Spotify's API, then fetches corresponding album tags and artist tags from LastFM's API

It then groups these into clusters (with default numerical names) which can be renamed. It uses a fine-tuned HDBSCAN algorithm.

There is a search button which searches by album name and artist name.

## Future Additions
- [ ] Automatic Cluster Naming
- [ ] Greater searching
- [ ] Automatic library updating
