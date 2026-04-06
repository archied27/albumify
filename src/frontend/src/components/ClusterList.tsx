import { useState, useEffect } from "react";
import { getClusters } from "../api/clusters";
import { useNavigate } from "react-router-dom";
import { Grid, Box, Skeleton, Typography } from "@mui/material";

type SimpleCluster = {
    id: string,
    name: string,
    count: number
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
        <Grid container spacing={2} p={2} display="block">
            {clusters ? clusters.map((cluster) => (
                <Grid key={cluster.id} >
                    <Box onClick={() => navigate(`/clusters/${cluster.id}`)}
                        sx={{
                            cursor: "pointer",
                            display: "flex",
                            flexDirection: "column",
                            justifyContent: "center",
                            alignItems: "left"
                        }}>
                        <Typography variant="body2" fontWeight={600}>{cluster.name}</Typography>
                        <Typography variant="caption" color="text.secondary">Albums: {cluster.count}</Typography>
                    </Box>
                </Grid>
                ))
        : <Skeleton variant="rectangular" width={"100%"}/>}
        </Grid>
    );
}