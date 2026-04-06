import { ClusterAlbumList } from "../components/ClusterAlbumList";
import { useParams } from "react-router-dom";

export function ClusterAlbumListPage()
{
    const { id } = useParams();
    if(!id) return <div>Invalid Cluster</div>

    return <ClusterAlbumList id={id}/>
}