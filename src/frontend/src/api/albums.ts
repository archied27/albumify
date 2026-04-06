import client from './client.ts'

type SimpleAlbum = {
    id: string,
    name: string,
    release_date: string,
    cover_path: string,
    artist_name: string,
    artist_id: string
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

export function getAlbums(): Promise<SimpleAlbum[]>
{
    return client.get<SimpleAlbum[]>("/albums/")
        .then(res => res.data);
}

export function getAlbumInfo(id: string): Promise<FullAlbum>
{
    return client.get<FullAlbum>(`/albums/${id}`).then(res => res.data);
}