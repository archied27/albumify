import { useState, useEffect, useRef } from "react";
import { getClusters, renameCluster } from "../api/clusters";
import { useNavigate } from "react-router-dom";
import { Grid, Box, Skeleton, Typography, IconButton, TextField } from "@mui/material";
import { Edit } from "@mui/icons-material";

type SimpleCluster = {
    id: string,
    name: string,
    count: number,
    cover_path: string
}

export function ClusterList()
{
    const [clusters, setClusters] = useState<SimpleCluster[] | null>(null);
    const [hoverId, setHoverId] = useState<string | null>(null);
    const [editingId, setEditingId] = useState<string | null>(null);
    const [editingName, setEditingName] = useState<string>("");
    const inputRef = useRef<HTMLInputElement>(null);

    const navigate = useNavigate();

    useEffect(() => {
        async function fetchClusters() {
            const data = await getClusters();
            setClusters(data);
        }
        fetchClusters();
    }, [])

    function handleEditClick(e: React.MouseEvent, cluster: SimpleCluster)
    {
        e.stopPropagation();
        setEditingId(cluster.id);
        setEditingName(cluster.name);
        setTimeout(() => {
            inputRef.current?.focus();
            inputRef.current?.select();
        }, 50);
    }

    async function handleRenameConfirm(e: React.MouseEvent) {
        e.stopPropagation();
        if (!editingId || !editingName.trim()) return;

        await renameCluster({"id": editingId, "name": editingName.trim()});

        setClusters(prev =>
            prev?.map(c => c.id === editingId ? { ...c, name: editingName.trim() } : c) ?? null
        );
        setEditingId(null);
    }

    function handleKeyDown(e: React.KeyboardEvent) {
        if (e.key === "Enter") handleRenameConfirm(e as any);
        if (e.key === "Escape") {
            setEditingId(null);
        }
    }

    return (
        <Grid container spacing={2} p={2} display="flex">
            {clusters ? clusters.map((cluster) => (
                <Grid key={cluster.id} size={{xs:4, sm:3, md:2}}>
                    <Box onClick={() => navigate(`/clusters/${cluster.id}`)}
                        onMouseEnter={() => setHoverId(cluster.id)}
                        onMouseLeave={() => {setHoverId(null) 
                            setEditingId(null)}}
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
                            {editingId === cluster.id ? (
                            <Box onClick={e => e.stopPropagation()}
                            sx={{ display: "flex", alignItems: "center", gap: 0.5, width: "100%", px: 1 }}>
                                <TextField 
                                    inputRef={inputRef}
                                    value={editingName}
                                    onChange={e => setEditingName(e.target.value)}
                                    onKeyDown={handleKeyDown}
                                    size="small"
                                    variant="standard"
                                    sx={{
                                        flex: 1,
                                        input: { color: "white", textAlign: "center", fontWeight: 700 },
                                        "& .MuiInput-underline:before": { borderBottomColor: "rgba(255,255,255,0.5)" },
                                        "& .MuiInput-underline:after": { borderBottomColor: "white" },
                                    }}/>
                            </Box>)  
                            
                            : (<Box sx={{ position: "relative", display: "flex",  alignItems: "center", justifyContent: "center", gap: 0.5}}>
                                <Typography variant="body1" fontWeight={700}>
                                    {cluster.name}
                                </Typography>

                                <IconButton size="small"
                                    onClick={e => handleEditClick(e, cluster)}
                                    sx={{
                                        color: "white",
                                        p: 0.75,
                                        opacity: hoverId === cluster.id ? 1 : 0,
                                        transition: "opacity 0.2s",
                                        position: "absolute",
                                        left: "100%"
                                    }}>
                                        <Edit sx={{ fontSize: 14 }}/>
                                </IconButton>
                            </Box> )}

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