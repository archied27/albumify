import client from './client.ts'

type SimpleCluster = {
    id: string,
    name: string,
    count: number,
    cover_path: string
}

type SimpleAlbum = {
    id: string,
    name: string,
    release_date: string,
    cover_path: string,
    artist_name: string,
    artist_id: string
}

type RenameInput = {
    id: string,
    name: string
}

type RenameResponse = {
    message: string
}

export function getClusters(): Promise<SimpleCluster[]>
{
    return client.get<SimpleCluster[]>("/clusters/")
        .then(res => res.data);
}

export function getClusterInfo(id: string): Promise<SimpleAlbum[]>
{
    return client.get<SimpleAlbum[]>(`/clusters/${id}`).then(res => res.data);
}

export function renameCluster(input: RenameInput): Promise<RenameResponse>
{
    return client.post<RenameResponse>(`/clusters/${input['id']}/${input['name']}`)
        .then(res => res.data);
}