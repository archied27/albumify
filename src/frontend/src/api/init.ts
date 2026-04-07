import client from "./client.ts"

type MessageResponse = {
    message: string
}

type RunningResponse = {
    message: string,
    stage: string
}

type Status = {
    running: boolean,
    stage: string | null,
    progress: string | null,
    done: boolean,
    error: string | null
}

export function getStatus(): Promise<Status>
{
    return client.get("/init/status")
        .then(res => res.data)
}

export function startInit(): Promise<MessageResponse | RunningResponse>
{
    return client.post("/init/")
        .then(res => res.data)
}

export function resetInit(): Promise<MessageResponse | RunningResponse>
{
    return client.post("/init/reset")
        .then(res => res.data)
}

export function recluster()
{
    return client.post("/init/recluster")
        .then(res => res.data)
}