import { useState, useEffect } from "react";
import { getClusters } from "../api/clusters";
import { useNavigate } from "react-router-dom";
import { Grid, Box, Skeleton, Typography } from "@mui/material";

type SimpleCluster = {
    id: string,
    name: string,
    count: number,
    cover_path: string
}

export function ClusterList()
{
    const [clusters, setClusters] = useState<SimpleCluster[] | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        async function fetchClusters() {
            const data = await getClusters();
            setClusters(data);
        }
        fetchClusters();
    }, [])

    return (
        <Grid container spacing={2} p={2} display="flex">
            {clusters ? clusters.map((cluster) => (
                <Grid key={cluster.id} size={{xs:4, sm:3, md:2}}>
                    <Box onClick={() => navigate(`/clusters/${cluster.id}`)}
                        sx={{
                            cursor: "pointer",
                            position: "relative",
                            overflow: "hidden",
                            borderRadius: 2,
                            "&:hover": { transform: "scale(1.05)" },
                            transition: "transform 0.2s",
                        }}>

                        <Box
                            component="img"
                            src={cluster.cover_path}
                            alt={cluster.name}
                            sx={{
                            width: "100%",
                            height: "auto",
                            objectFit: "cover",
                            display: "block",
                            }} />

                        <Box
                            sx={{
                            position: "absolute",
                            top: 0,
                            left: 0,
                            width: "100%",
                            height: "100%",
                            backgroundColor: "rgba(0,0,0,0.5)", 
                            }} />
                        
                        <Box
                            sx={{
                            position: "absolute",
                            top: 0,
                            left: 0,
                            width: "100%",
                            height: "100%",
                            display: "flex",
                            flexDirection: "column",
                            justifyContent: "center",
                            alignItems: "center",
                            textAlign: "center",
                            color: "white",
                            px: 1,
                            }}
                        >
                            <Typography variant="body1" fontWeight={700}>
                            {cluster.name}
                            </Typography>
                            <Typography variant="caption">
                            Albums: {cluster.count}
                            </Typography>
                        </Box>

                    </Box>
                </Grid>
                ))
        : <Skeleton variant="rectangular" width={"100%"}/>}
        </Grid>
    );
}