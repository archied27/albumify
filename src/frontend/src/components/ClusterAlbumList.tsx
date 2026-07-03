import { useState, useEffect } from "react";
import { getClusterInfo } from "../api/clusters";
import { Box, Grid, Typography, Skeleton } from "@mui/material";
import { useNavigate } from "react-router-dom";

type ClusterAlbumListProps = { id: string }

type SimpleAlbum = {
    id: string,
    name: string,
    release_date: string,
    cover_path: string,
    artist_name: string,
    artist_id: string
}

export function ClusterAlbumList({ id }: ClusterAlbumListProps)
{
    const [albums, setAlbums] = useState<SimpleAlbum[] | null>(null)
    const navigate = useNavigate();

    useEffect(() => {
        async function fetchAlbums(id: string) {
            const data = await getClusterInfo(id);
            setAlbums(data);
        }
        fetchAlbums(id);
    }, [])

    return (
        <Grid container spacing={2} p={2}>
      {albums ? albums.map((album) => (
        <Grid key={album.id} size={{xs:6, sm:3, md:2}}> 
          <Box onClick={() => navigate(`/albums/${album.id}`)}
            sx={{
            cursor: "pointer",
            "&:hover": { transform: "scale(1.05)"},
            display: "flex",
            flexDirection: "column",
            transition: "transform 0.2s",
            justifyContent: "center",
            alignItems: "center"
          }}>
            <img src={album.cover_path} alt={album.name} style={{ width: "100%", height:"auto", borderRadius: 8}}/>
            <Typography variant='body2' mt={1} fontWeight={600} textAlign="center">{album.name}</Typography>
            <Typography variant='caption' color='text.secondary'>{album.artist_name}</Typography>
            <Typography variant='caption' color='text.secondary'>{album.release_date}</Typography>
          </Box>
        </Grid>
      )) : <Skeleton variant='rectangular' height={100}/> }
    </Grid>
    )
}