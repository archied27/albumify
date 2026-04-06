import { useState, useEffect } from "react";
import { getAlbumInfo } from "../api/albums";
import { Box, Grid, Skeleton, Typography } from "@mui/material";

type AlbumInfoProps = {
    id: string
}

type Tag = {
    tag: string,
    weight: number
}

type Artist = {
    name: string,
    id: string
}

type FullAlbum = {
    name: string,
    url: string,
    cover_path: string,
    cluster: number,
    release_date: string,
    popularity: number,
    artists: Artist[],
    genres: string[],
    tags: Tag[]
}

export function AlbumInfo({ id }: AlbumInfoProps)
{
    const [album, setAlbum] = useState<FullAlbum | null>(null);

    useEffect(() => {
        async function fetchAlbum(id: string) {
            const data = await getAlbumInfo(id);
            setAlbum(data);
        }
        fetchAlbum(id)
    }, [])

    return(
        <Grid container spacing={2} p={2}>
            {album ?

            <Box sx={{ display: "flex", flexDirection: { xs: "column", md: "row" }, p: 4, gap: 4 }}>
                <Box sx={{ flex: 1, display: "flex", justifyContent: "center" }}>
                    <img src={album.cover_path} alt={album.name}
                    style={{width: "100%", maxWidth: 400, borderRadius: 8}}/>
                </Box>

                <Box sx={{ flex: 1, display: "flex", flexDirection: "column", gap: 2 }}>
                    <a href={album.url} style={{color: "inherit", textDecoration: "none"}}><Typography variant="h4" fontWeight={600}>{album.name}</Typography></a>
                    {album.artists.map((artist) => 
                        <Typography variant="subtitle1" color="text.secondary">{artist.name}</Typography>)}

                    <Typography variant="body2" fontWeight={500}>Cluster {album.cluster}</Typography>
                    <Typography variant="body2" color="text.secondary">{album.release_date}</Typography>
                    
                    {(album.genres[0]) ? 
                        <Box>
                            <Typography variant="subtitle2" fontWeight={500}>Genres:</Typography>
                            <Box sx={{display: "flex", flexWrap: "wrap", gap: 1, mt:1}}>
                                {album.genres.map((genre) => (
                                    <Typography key={genre} variant="caption" sx={{ backgroundColor: "#393838", px:1, borderRadius: 1 }}>
                                        {genre}
                                    </Typography>
                                ))}
                            </Box>
                        </Box>
                    : <></>}

                    {(album.tags[0]) ?
                    <Box>
                        <Typography variant="subtitle2" fontWeight={500}>Tags:</Typography>
                        <Box sx={{display: "flex", flexWrap: "wrap", gap: 1, mt:1}}>
                            {album.tags.map((tag) => (
                                <Typography key={tag.tag} variant="caption" sx={{ backgroundColor: "#393838", px:1, borderRadius: 1 }}>
                                    {tag.tag} · {tag.weight}
                                </Typography>
                            ))}
                        </Box>
                    </Box>
                    : <></>}

                    <Typography variant="body2">Popularity: {album.popularity}</Typography>

                </Box>
            </Box>

            : <Skeleton/>}
        </Grid>
    )
}