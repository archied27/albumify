import { AlbumInfo } from "../components/AlbumInfo";
import { useParams } from "react-router-dom";

export function FullAlbumPage() 
{
    const { id } = useParams();
    if(!id) return <div>Invalid Id</div>

    return <AlbumInfo id={id}/>
}