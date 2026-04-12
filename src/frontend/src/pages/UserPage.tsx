import { useState, useEffect } from "react";
import { getAuthStatus, auth } from "../api/auth";
import { startInit, resetInit, getStatus, recluster } from "../api/init";
import { Button, Typography, Grid, Box, Skeleton, LinearProgress } from "@mui/material";

type Status = {
    running: boolean,
    stage: string | null,
    progress: string | null,
    done: boolean,
    error: string | null
}

export function UserPage()
{
    const [authenticated, setAuthenticated] = useState<boolean>(false)
    const [status, setStatus] = useState<Status | null>(null);

    useEffect(() => {
        async function getAuth() {
            const data = await getAuthStatus();
            setAuthenticated(data["authenticated"]);
        }
        getAuth();

        async function getCurrentStatus() {
            const data = await getStatus();
            setStatus(data);
        }
        getCurrentStatus();
        const interval = setInterval(getCurrentStatus, 1000);
        return () => clearInterval(interval);
    }, [])

    async function handleAuth() {
        await auth();
    }

    function getProgressPercent(progress: string | null): number {
        if (!progress) return 0;
        const match = progress.match(/(\d+)\/(\d+)/);
        if (!match) return 0;
        const done = parseInt(match[1], 10);
        const total = parseInt(match[2], 10);
        return total > 0 ? (done / total) * 100 : 0;
    }

    return (
        <Grid display="flex" justifyContent="center" flexDirection="column" alignItems="center" p={2} gap={2}>
            <Button onClick={() => recluster()}
            sx={{color: "text.secondary", bgcolor: "#393838"}}>Recluster</Button>
            { (authenticated) ? 
        <Box display="flex" justifyContent="center" flexDirection="column" gap={2}>
            <Typography>Logged In With Spotify</Typography>
            
            <Button onClick={() => resetInit()}
            sx={{color: "white", bgcolor:"red"}}>RESET ALBUMS</Button>

            { status ? (status["done"] ? 
            <Typography>Initialisation Complete</Typography> : 
            status["running"] ? 

            <Box display="flex" justifyContent="center" flexDirection="column" gap={2} alignItems="center">
                <Typography variant="subtitle1" fontWeight={600} color="text.primary">
                    {status.stage}
                </Typography>
                {status["progress"] ?
                <>
                    <Typography variant="body2" color="text.secondary">
                        {status["progress"]}
                    </Typography>
                    <LinearProgress
                        variant="determinate"
                        value={getProgressPercent(status.progress)}
                        color="success"
                        sx={{ width: "100%", borderRadius: 1 }}/>
                </>: <></>
                }
            </Box>

            :
            <>
                <Button onClick={() => startInit()}
                sx={{color: "text.secondary", bgcolor: "#393838"}}>Start Initialisation</Button>
                {status["error"] ? <Typography color="error">{status["error"]}</Typography> : <></>}
                
            </>
            ): 
            <Skeleton variant="rectangular" height={"100%"} />}
        </Box>

         : 
            <Button onClick={() => handleAuth()}
            sx={{color: "text.secondary", bgcolor: "#393838"}}>Login With Spotify</Button>}
        </Grid>

    )
}