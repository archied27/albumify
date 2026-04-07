import {  SearchList } from "../components/SearchList"
import { useSearchParams } from "react-router-dom";

export function SearchListPage() 
{
    const [searchParams] = useSearchParams();
    const q = searchParams.get('q');
    
    if(!q) return <div>Invalid Id</div>

    return <SearchList q={q}/>
}